%% Construct and Initialize Gripper
% Init should only be run once per object: if ran multiple times, 
% errors may occur
grip = RobotiqGripper;
grip.init('COM9');

%% Define constants for speed, force, position
GripSpeed = 120;
GripForce = 255;
GripOpen = 0;
GripClosed = 255;

%% Set the gripper traits to the constants
grip.Speed = GripSpeed;
grip.Force = GripForce;

%% Set the gripper to open and close
while true
    grip.Position = GripOpen;
    pause(2);
    grip.Position = GripClosed;
    pause(2);
end