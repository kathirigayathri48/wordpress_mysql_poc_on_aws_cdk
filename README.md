# wordpress_mysql_poc_on_aws_cdk

(.venv) root@oshvm:~/wp_mysql# cdk synth
[Warning at /WpMysqlStack/myASG] desiredCapacity has been configured. Be aware this will reset the size of your AutoScalingGroup on every deployment. See https://github.com/aws/aws-cdk/issues/5215
Resources:
  myrdssg5EE3ADCC:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: WpMysqlStack/my_rds_sg
      SecurityGroupEgress:
        - CidrIp: 0.0.0.0/0
          Description: Allow all outbound traffic by default
          IpProtocol: "-1"
      VpcId: vpc-439e5728
    Metadata:
      aws:cdk:path: WpMysqlStack/my_rds_sg/Resource
  mysg143CED9A:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: WpMysqlStack/my_sg
      SecurityGroupEgress:
        - CidrIp: 0.0.0.0/0
          Description: Allow all outbound traffic by default
          IpProtocol: "-1"
      SecurityGroupIngress:
        - CidrIp: 0.0.0.0/0
          Description: allow ssh access from the world
          FromPort: 22
          IpProtocol: tcp
          ToPort: 22
        - CidrIp: 0.0.0.0/0
          Description: allow ssh access from the world
          FromPort: 80
          IpProtocol: tcp
          ToPort: 80
      VpcId: vpc-439e5728
    Metadata:
      aws:cdk:path: WpMysqlStack/my_sg/Resource
  myEC2InstanceRole116EFD8E:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
        Version: "2012-10-17"
      Tags:
        - Key: Name
          Value: mywpHost
    Metadata:
      aws:cdk:path: WpMysqlStack/myEC2/InstanceRole/Resource
  myEC2InstanceProfile2D3B3519:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - Ref: myEC2InstanceRole116EFD8E
    Metadata:
      aws:cdk:path: WpMysqlStack/myEC2/InstanceProfile
  myEC27742CD16:
    Type: AWS::EC2::Instance
    Properties:
      AvailabilityZone: ap-south-1a
      IamInstanceProfile:
        Ref: myEC2InstanceProfile2D3B3519
      ImageId:
        Ref: SsmParameterValueawsserviceamiamazonlinuxlatestamzn2amihvmx8664gp2C96584B6F00A464EAD1953AFF4B05118Parameter
      InstanceType: t2.micro
      KeyName: wordpress_ec2_key
      SecurityGroupIds:
        - Fn::GetAtt:
            - mysg143CED9A
            - GroupId
      SubnetId: subnet-05788f6e
      Tags:
        - Key: Name
          Value: mywpHost
      UserData:
        Fn::Base64: |
          #!/bin/bash
          sudo yum update -y
          sudo yum install -y mysql httpd
          sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
          sudo service httpd start
          wget https://wordpress.org/latest.tar.gz
          tar -xzf latest.tar.gz
          cd wordpress
          cp wp-config-sample.php wp-config.php
          sudo cp -r /wordpress/* /var/www/html/
          sudo service httpd restart
    DependsOn:
      - myEC2InstanceRole116EFD8E
    Metadata:
      aws:cdk:path: WpMysqlStack/myEC2/Resource
  myALB18A49813:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      LoadBalancerAttributes:
        - Key: deletion_protection.enabled
          Value: "false"
      Name: myALB
      Scheme: internet-facing
      SecurityGroups:
        - Fn::GetAtt:
            - myALBSecurityGroupF245F258
            - GroupId
      Subnets:
        - subnet-05788f6e
        - subnet-39d6f275
        - subnet-5566082e
      Type: application
    Metadata:
      aws:cdk:path: WpMysqlStack/myALB/Resource
  myALBSecurityGroupF245F258:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Automatically created Security Group for ELB WpMysqlStackmyALBCC2B1C90
      SecurityGroupIngress:
        - CidrIp: 0.0.0.0/0
          Description: Internet access ALB 80
          FromPort: 80
          IpProtocol: tcp
          ToPort: 80
      VpcId: vpc-439e5728
    Metadata:
      aws:cdk:path: WpMysqlStack/myALB/SecurityGroup/Resource
  myALBSecurityGrouptoWpMysqlStackmyASGInstanceSecurityGroup4CB365FC807EA48197:
    Type: AWS::EC2::SecurityGroupEgress
    Properties:
      GroupId:
        Fn::GetAtt:
          - myALBSecurityGroupF245F258
          - GroupId
      IpProtocol: tcp
      Description: ALB access 80 port of EC2 in Autoscaling Group
      DestinationSecurityGroupId:
        Fn::GetAtt:
          - myASGInstanceSecurityGroup77B88BA5
          - GroupId
      FromPort: 80
      ToPort: 80
    Metadata:
      aws:cdk:path: WpMysqlStack/myALB/SecurityGroup/to WpMysqlStackmyASGInstanceSecurityGroup4CB365FC:80
  myALBmy80B990410C:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - TargetGroupArn:
            Ref: myALBmy80addTargetGroupGroup1569733D
          Type: forward
      LoadBalancerArn:
        Ref: myALB18A49813
      Port: 80
      Protocol: HTTP
    Metadata:
      aws:cdk:path: WpMysqlStack/myALB/my80/Resource
  myALBmy80addTargetGroupGroup1569733D:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Port: 80
      Protocol: HTTP
      TargetType: instance
      VpcId: vpc-439e5728
    Metadata:
      aws:cdk:path: WpMysqlStack/myALB/my80/addTargetGroupGroup/Resource
  myASGInstanceSecurityGroup77B88BA5:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: WpMysqlStack/myASG/InstanceSecurityGroup
      SecurityGroupEgress:
        - CidrIp: 0.0.0.0/0
          Description: Allow all outbound traffic by default
          IpProtocol: "-1"
      Tags:
        - Key: Name
          Value: WpMysqlStack/myASG
      VpcId: vpc-439e5728
    Metadata:
      aws:cdk:path: WpMysqlStack/myASG/InstanceSecurityGroup/Resource
  myASGInstanceSecurityGroupfromWpMysqlStackmyALBSecurityGroup6E44C1F780CB1FF16B:
    Type: AWS::EC2::SecurityGroupIngress
    Properties:
      IpProtocol: tcp
      Description: ALB access 80 port of EC2 in Autoscaling Group
      FromPort: 80
      GroupId:
        Fn::GetAtt:
          - myASGInstanceSecurityGroup77B88BA5
          - GroupId
      SourceSecurityGroupId:
        Fn::GetAtt:
          - myALBSecurityGroupF245F258
          - GroupId
      ToPort: 80
    Metadata:
      aws:cdk:path: WpMysqlStack/myASG/InstanceSecurityGroup/from WpMysqlStackmyALBSecurityGroup6E44C1F7:80
  myASGInstanceRole5AF7F92F:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
        Version: "2012-10-17"
      Tags:
        - Key: Name
          Value: WpMysqlStack/myASG
    Metadata:
      aws:cdk:path: WpMysqlStack/myASG/InstanceRole/Resource
  myASGInstanceProfile053766AB:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - Ref: myASGInstanceRole5AF7F92F
    Metadata:
      aws:cdk:path: WpMysqlStack/myASG/InstanceProfile
  myASGLaunchConfigA0CD8C73:
    Type: AWS::AutoScaling::LaunchConfiguration
    Properties:
      ImageId:
        Ref: SsmParameterValueawsserviceamiamazonlinuxlatestamzn2amihvmx8664gp2C96584B6F00A464EAD1953AFF4B05118Parameter
      InstanceType: t2.micro
      IamInstanceProfile:
        Ref: myASGInstanceProfile053766AB
      KeyName: wordpress_ec2_key
      SecurityGroups:
        - Fn::GetAtt:
            - myASGInstanceSecurityGroup77B88BA5
            - GroupId
      UserData:
        Fn::Base64: |
          #!/bin/bash
          sudo yum update -y
          sudo yum install -y mysql httpd
          sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
          sudo service httpd start
          wget https://wordpress.org/latest.tar.gz
          tar -xzf latest.tar.gz
          cd wordpress
          cp wp-config-sample.php wp-config.php
          sudo cp -r /wordpress/* /var/www/html/
          sudo service httpd restart
    DependsOn:
      - myASGInstanceRole5AF7F92F
    Metadata:
      aws:cdk:path: WpMysqlStack/myASG/LaunchConfig
  myASG6C9F5AC0:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      MaxSize: "2"
      MinSize: "2"
      DesiredCapacity: "2"
      LaunchConfigurationName:
        Ref: myASGLaunchConfigA0CD8C73
      Tags:
        - Key: Name
          PropagateAtLaunch: true
          Value: WpMysqlStack/myASG
      TargetGroupARNs:
        - Ref: myALBmy80addTargetGroupGroup1569733D
      VPCZoneIdentifier:
        - subnet-05788f6e
        - subnet-39d6f275
        - subnet-5566082e
    UpdatePolicy:
      AutoScalingScheduledAction:
        IgnoreUnmodifiedGroupSizeProperties: true
    Metadata:
      aws:cdk:path: WpMysqlStack/myASG/ASG
  CDKMetadata:
    Type: AWS::CDK::Metadata
    Properties:
      Analytics: v2:deflate64:H4sIAAAAAAAAA2VQzU7DMAx+lt2zjIA0iRswITRph6rjBUzmdmZpUiUOaKry7qQtnVo42d9PPttRslNKybvVE3yHtT5dNtp5lN2RQV9EicFFr1HsKluAhwYZvdg5G9hHzT09WZJQajvP6WuH+j5noY6e+PrmXWz7N0tin9PAjkPm/cL1WnsM4R+9twOfBEEju9KZ4eVUp7TCu4pMXhENBCZtHJw+wGSJbP2VN3xuW0MamJw9ZO1l0PpLqyWe+ygw2l/P1M/0d/A18u3kGUwCIrugweTpeXYGxxHc3AeIVp/zP1dURz/k9fRfa0pJFFc+O7t5kFv5uPoMRGsfLVODshzrD970dQbiAQAA
    Metadata:
      aws:cdk:path: WpMysqlStack/CDKMetadata/Default
Parameters:
  SsmParameterValueawsserviceamiamazonlinuxlatestamzn2amihvmx8664gp2C96584B6F00A464EAD1953AFF4B05118Parameter:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2
	
============================================================================

(.venv) root@oshvm:~/wp_mysql# cdk deploy
[Warning at /WpMysqlStack/myASG] desiredCapacity has been configured. Be aware this will reset the size of your AutoScalingGroup on every deployment. See https://github.com/aws/aws-cdk/issues/5215
This deployment will make potentially sensitive changes according to your current security approval level (--require-approval broadening).
Please confirm you intend to make the following modifications:

IAM Statement Changes
┌───┬───────────────────────────┬────────┬────────────────┬───────────────────────────┬───────────┐
│   │ Resource                  │ Effect │ Action         │ Principal                 │ Condition │
├───┼───────────────────────────┼────────┼────────────────┼───────────────────────────┼───────────┤
│ + │ ${myASG/InstanceRole.Arn} │ Allow  │ sts:AssumeRole │ Service:ec2.amazonaws.com │           │
├───┼───────────────────────────┼────────┼────────────────┼───────────────────────────┼───────────┤
│ + │ ${myEC2/InstanceRole.Arn} │ Allow  │ sts:AssumeRole │ Service:ec2.amazonaws.com │           │
└───┴───────────────────────────┴────────┴────────────────┴───────────────────────────┴───────────┘
Security Group Changes
┌───┬────────────────────────────────────────┬─────┬────────────┬────────────────────────────────────────┐
│   │ Group                                  │ Dir │ Protocol   │ Peer                                   │
├───┼────────────────────────────────────────┼─────┼────────────┼────────────────────────────────────────┤
│ + │ ${myALB/SecurityGroup.GroupId}         │ In  │ TCP 80     │ Everyone (IPv4)                        │
│ + │ ${myALB/SecurityGroup.GroupId}         │ Out │ TCP 80     │ ${myASG/InstanceSecurityGroup.GroupId} │
├───┼────────────────────────────────────────┼─────┼────────────┼────────────────────────────────────────┤
│ + │ ${myASG/InstanceSecurityGroup.GroupId} │ In  │ TCP 80     │ ${myALB/SecurityGroup.GroupId}         │
│ + │ ${myASG/InstanceSecurityGroup.GroupId} │ Out │ Everything │ Everyone (IPv4)                        │
├───┼────────────────────────────────────────┼─────┼────────────┼────────────────────────────────────────┤
│ + │ ${my_rds_sg.GroupId}                   │ Out │ Everything │ Everyone (IPv4)                        │
├───┼────────────────────────────────────────┼─────┼────────────┼────────────────────────────────────────┤
│ + │ ${my_sg.GroupId}                       │ In  │ TCP 22     │ Everyone (IPv4)                        │
│ + │ ${my_sg.GroupId}                       │ In  │ TCP 80     │ Everyone (IPv4)                        │
│ + │ ${my_sg.GroupId}                       │ Out │ Everything │ Everyone (IPv4)                        │
└───┴────────────────────────────────────────┴─────┴────────────┴────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)

Do you wish to deploy these changes (y/n)? y
WpMysqlStack: deploying...
WpMysqlStack: creating CloudFormation changeset...

 ✅  WpMysqlStack

Stack ARN:
arn:aws:cloudformation:ap-south-1:504357410036:stack/WpMysqlStack/5ac0d680-f096-11eb-b3ae-0aef5eb06ea6
(.venv) root@oshvm:~/wp_mysql#

(.venv) root@oshvm:~/wp_mysql# cdk ls
WpMysqlStack
(.venv) root@oshvm:~/wp_mysql#

************************
(.venv) root@oshvm:~/wp_mysql# cdk destroy
Are you sure you want to delete: WpMysqlStack (y/n)? y
WpMysqlStack: destroying...

 ✅  WpMysqlStack: destroyed
(.venv) root@oshvm:~/wp_mysql#
