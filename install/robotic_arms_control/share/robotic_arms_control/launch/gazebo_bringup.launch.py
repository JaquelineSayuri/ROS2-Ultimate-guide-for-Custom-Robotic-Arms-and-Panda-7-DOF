from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get the path to the package and the URDF file
    pkg_description = get_package_share_directory('robotic_arms_control')
    urdf_file = os.path.join(pkg_description, "urdf", 'bazu.urdf')

    # Read the URDF file
    with open(urdf_file, 'r') as file:
        urdf_content = file.read()

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="RSP",
        output="screen",
        parameters=[{'robot_description': urdf_content}]
    )

    gazebo_bringup = ExecuteProcess(
        cmd=["gazebo", "--verbose", "-s", "libgazebo_ros_factory.so"],
        output="screen"
    )

    # Spawn the entity in Gazebo
    spawn_node = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "/robot_description", "-entity", "bazu"],
        output="screen"
    )

    # Return the LaunchDescription
    return LaunchDescription([
        robot_state_publisher_node,
        gazebo_bringup,
        spawn_node
    ])

if __name__ == '__main__':
    generate_launch_description()