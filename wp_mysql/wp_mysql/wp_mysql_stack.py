from aws_cdk import core as cdk
import aws_cdk.aws_ec2 as ec2
#import aws_cdk.aws_rds as rds
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

vpc_id = "vpc-439e5728"
ec2_type = "t2.micro"
key_name = "wordpress_ec2_key"
linux_ami = ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
                )

with open("./user_data/user_data.sh") as f:
    user_data = f.read()

class WpMysqlStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get vpc object corresponding to defined vpc id
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)

        #Create a security group for rds and wordpress
        rds_security_group = ec2.SecurityGroup(self, "my_rds_sg",
                                                  vpc=vpc,
                                                  allow_all_outbound=True,
                                                  )
        wp_security_group = ec2.SecurityGroup(self, "my_sg",
                                                  vpc=vpc,
                                                  allow_all_outbound=True,
                                                  )

        # Add ingress rules for wordpress security group
        wp_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")
        wp_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "allow ssh access from the world")

        # Get Security group object from hardcoded security group
        #security_group=ec2.SecurityGroup.from_lookup(self, "EC2", security_group_id=security_group_id)


        '''
        # Create rds instance with mysql engine
        rds.DatabaseInstance(
            self, "RDS",
            database_name="my_rds_mysql",
            security_groups=[rds_security_group],
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_16
            ),
            vpc=vpc,
            port=3306,
            instance_type= ec2.InstanceType.of(
                ec2.InstanceClass.MEMORY4,
                ec2.InstanceSize.LARGE,
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False
        ),
        '''
        host = ec2.Instance(self, "myEC2",
                            security_group=wp_security_group,
                            instance_type=ec2.InstanceType(
                                instance_type_identifier=ec2_type),
                            instance_name="mywpHost",
                            machine_image=linux_ami,
                            vpc=vpc,
                            key_name=key_name,
                            user_data=ec2.UserData.custom(user_data),
                            vpc_subnets=ec2.SubnetSelection(
                                subnet_type=ec2.SubnetType.PUBLIC),
                            )
        # Create ALB
        alb = elb.ApplicationLoadBalancer(self, "myALB",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="myALB"
                                          )
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        listener = alb.add_listener("my80",
                                    port=80,
                                    open=True)

        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg = autoscaling.AutoScalingGroup(self, "myASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                                )

        self.asg.connections.allow_from(alb, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])
