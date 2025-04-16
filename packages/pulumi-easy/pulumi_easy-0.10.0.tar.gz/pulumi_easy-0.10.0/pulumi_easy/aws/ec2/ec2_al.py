import pulumi
from .ec2 import EC2Manager

class EC2AL(EC2Manager):
    """
    Class for managing AWS EC2 Amazon Linux instances with Pulumi.
    Extends EC2Manager with Amazon Linux-specific instance creation capabilities.
    """
    
    def create_amazon_linux_instance(self, name: str, storage: int, version: str, 
                            arch: str, instance_type: str, ssh_key_name: str,
                            security_group=None, iam_instance_profile=None,
                            my_ipv4=None, my_ipv6=None, additional_tags=None, user_data=None,
                            subnet_id=None, vpc_id=None):
        """
        Creates an Amazon Linux EC2 instance with specified parameters.
        
        Args:
            name (str): Name for the EC2 instance
            storage (int): Root EBS volume size in GB
            version (str): Amazon Linux version (e.g., "2" or "3")
            arch (str): Architecture (e.g., "x86_64", "arm64")
            instance_type (str): EC2 instance type (e.g., "t2.micro", "t4g.nano")
            ssh_key_name (str): Name of the SSH key pair to use
            security_group (aws.ec2.SecurityGroup, optional): Custom security group. 
                If not provided, a default one will be created.
            iam_instance_profile (str, optional): The IAM instance profile to associate 
                with the instance.
            my_ipv4 (str, optional): Your IPv4 address for restricted SSH access (e.g., "203.0.113.1/32")
            my_ipv6 (str, optional): Your IPv6 address for restricted SSH access (e.g., "2001:DB8::1/128")
            additional_tags (dict, optional): Additional tags to apply to the instance
            user_data (str, optional): User data script to run at launch time
            subnet_id (str, optional): ID of the subnet to launch the instance in.
                If provided, the instance will be launched in a VPC
            vpc_id (str, optional): ID of the VPC where security group should be created.
                Required when subnet_id is provided and security_group is not
            
        Returns:
            aws.ec2.Instance: The created EC2 instance resource
            
        Example:
            ```python
            ec2_al = EC2AL()
            # Standard instance
            instance1 = ec2_al.create_amazon_linux_instance(
                name="app-server",
                storage=20,
                version="2",
                arch="x86_64",
                instance_type="t2.micro",
                ssh_key_name="my-key-pair"
            )
            
            # VPC instance in a specific subnet
            instance2 = ec2_al.create_amazon_linux_instance(
                name="vpc-app-server",
                storage=20,
                version="3",
                arch="arm64",
                instance_type="t4g.nano",
                ssh_key_name="my-key-pair",
                subnet_id=vpc.private_subnets[0].id,
                vpc_id=vpc.vpc.id
            )
            ```
        """
        ami = self.get_amazon_linux_ami(version, arch)
        
        # Check for architecture compatibility
        is_arm_instance = any(arm_prefix in instance_type for arm_prefix in ["a1.", "t4g.", "c6g.", "c7g.", "m6g.", "r6g.", "x2gd."])
        is_arm_ami = "arm64" in arch
        
        if is_arm_instance and not is_arm_ami:
            pulumi.log.warn(f"WARNING: You are using an ARM-based instance type ({instance_type}) with a non-ARM AMI. This may fail.")
        elif not is_arm_instance and is_arm_ami:
            pulumi.log.warn(f"WARNING: You are using an x86 instance type ({instance_type}) with an ARM AMI. This will likely fail.")
        
        # Set default additional tags with OS info
        os_tags = {
            "OS": "AmazonLinux",
            "Version": version,
            "Architecture": arch
        }
        
        # Merge with provided additional tags if they exist
        if additional_tags:
            os_tags.update(additional_tags)
        
        # Root device for Amazon Linux is typically /dev/xvda
        root_device = "/dev/xvda"
            
        return self.create_instance(
            name=name,
            ami_id=ami.id,
            storage=storage,
            instance_type=instance_type,
            ssh_key_name=ssh_key_name,
            security_group=security_group,
            iam_instance_profile=iam_instance_profile,
            my_ipv4=my_ipv4,
            my_ipv6=my_ipv6,
            additional_tags=os_tags,
            user_data=user_data,
            root_device_name=root_device,
            subnet_id=subnet_id,
            vpc_id=vpc_id
        )
