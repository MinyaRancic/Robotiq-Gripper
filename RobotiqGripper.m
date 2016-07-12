classdef RobotiqGripper < matlab.mixin.SetGet
    %    Matlab class to control the robotiq 2-finger gripper
    %    class sends arguments to a python script that controls the gripper
    %    over rs-485 serial.
    %    
    %    obj = RobotiqGripper creates a RobotiqGripper object to connect to
    %    a Robotiq 2-finger adaptive gripper
    %
    % RobotiqGripper Methods
    %    init        - Initialize the RobotiqGripper object.
    %    get         - Query properties of the RobotiqGripper object.
    %    delete      - Uninitialize and remove the RobotiqGripper object.
    %    objDetect   - Returns whether or not an object has been detected.
    %Position
    % RobotiqGripper Properties 
    %    Position    - the  of the gripper between 0 and 255
    %    Speed       - the Speed of the gripper between 0 and 255
    %    Force       - the Force of the gripper between 0 and 255
    %    PyControl   - a python module object that contains the Robotiq.py
    %                  script
    %    IsInit      - a boolean that is true if the gripper has finished 
    %                  initializing
    %    Current     - the Current going through the motor of the gripper
    %    Fault       - the current fault status of the gripper
    %    Status      - the status of the gripper
    %
    % Example:
    %    % Create, Initialize, and close
    %    Grip = RobotiqGripper;
    %    Grip.init;
    %    set(grip, 'Position', 255);
    %  M. Rancic, 2016
    
    %----------------------------------------------------------------------
    %% General Properties
    %----------------------------------------------------------------------
    properties(SetAccess = 'public', GetAccess = 'public')
        Position    %int16 position of gripper from 0-255
        Speed       %int16 speed of gripper from 0-255
        Force       %int16 force of gripper from 0-255
        PyControl   %Python Module that communicates with the gripper
        IsInit      %boolean storing initilization status
        Current     %the Current through motorws in mA
        Fault       %Fault status of the gripper
        Status      %
    end
    %----------------------------------------------------------------------
    %% Constructor, destructor, and init. 
    %----------------------------------------------------------------------
    methods(Access = 'public')
        function obj = RobotiqGripper
            obj.IsInit = false;
        end
        
        function delete(obj)
            obj.PyControl.closeSerial();
            delete(obj);
        end
        
        function init(obj)
            if count(py.sys.path,'') == 0
                insert(py.sys.path,int32(0),'');
            end
            try
                obj.PyControl = py.importlib.import_module('robotiq');
            catch
                error('Cannot find the python class in your path. Are you sure you have it downloaded?');
            end
            py.reload(obj.PyControl);
            obj.PyControl.init();
            obj.IsInit = true;
            pause(.01);
            obj.Speed = int16(255);
            obj.Force = int16(255);
            obj.Position = int16(0);
        end
    end
    
    %% Get functions. Speed queries gripper, Force and Pos read propety
    methods
        function Position = get.Position(obj)
            if(obj.IsInit)
                response = obj.PyControl.checkStatus()
                Position = int16(hex2dec(char(response(15:16))));                 
                %Position = obj.Position;
            else
                error('Must run init() first.')
            end
        end
        
        function Speed = get.Speed(obj)
            if(obj.IsInit)
                Speed = obj.Speed;               
            else
                error('Must run init() first.')
            end
        end
        
        function Force = get.Force(obj)
            if(obj.IsInit)
                Force = obj.Force;               
            else
                error('Must run init() first.')
            end
        end
        
        function IsInit = get.IsInit(obj)
            IsInit = obj.IsInit;
        end

        %% Set Functions: All check for initilization before running
        function set.Position(obj, value)
            if(obj.IsInit)
                %obj.Position = int16(value);
                obj.PyControl.setPosition(int16(value));
            else
                error('Must run init() first.')
            end
        end
        
        function set.Speed(obj, value)
            if(obj.IsInit)
                obj.PyControl.setSpeed(int16(value));
                obj.Speed = int16(value);
            else
                error('Must run init() first.')
            end
        end
        
        function set.Force(obj, value)
            if(obj.IsInit)
                obj.PyControl.setForce(int16(value));
%                 obj.Force = int16(value);
            else
                error('Must run init() first.');
            end
        end
        
        %% Other Gripper functions.
        function fault = get.Fault(obj)
            response = obj.PyControl.checkStatus();
            tFault = char(response);
            tFault = tFault(11:12);
            switch(tFault)
                case '0'
                    fault = 'No fault';
                case '5'
                    fault = 'Action delayed, activation (reactivation) must be completed prior to renewed action.';
                case '7'
                    fault = 'The activation bit must be set prior to action';
                case '8'
                    fault = 'Maximum operating temperature exceeded, wait for cool-down.';
                case 'A'
                    fault = 'Under minimum operating voltage.';
                case 'B'
                    fault = 'Automatic release in progress.';
                case 'C'
                    fault = 'Internal processor fault';
                case 'D'
                    fault = 'Activation fault, verify that no interference or other error occurred.';
                case 'E'
                    fault = 'Overcurrent triggered.';
                case 'F'
                    fault = ' Automatic release completed.';
                otherwise
                    fault = 'this shouldn''t have happened but do''t worry about it';
            end
        end
        
        function current = get.Current(obj)
            response = obj.PyControl.checkStatus();
            tCurrent = char(response);
            current = hex2dec(tCurrent(17:18));
        end
        
        function detect = objDetection(obj)
            response = obj.PyControl.checkStatus();
            tDetect = char(response);
            tDetect = dec2bin(hex2dec(tDetect(7)));
            tDetect = bin2dec(tDetect(3:4));
            switch tDetect
                case 0
                    detect = false;
                case 1
                    detect = true;
                case 2
                    detect = true;
                case 3
                    detect = false;
                otherwise
                    error('Something went wrong while object detecting.');
            end
        end
        
        function status = get.Status(obj)
            response = obj.PyControl.checkStatus();
            tStatus = char(response);
            tStatus = dec2bin(hex2dec(tStatus(7)));
            tStatus = bin2dec(tStatus(3:4));
            switch tStatus
                case 0
                    status = 'Gripper is in reset ( or automatic release ) state. See Fault Status if Gripper is activated.';
                case 1
                    status = 'Activation in progress.';
                case 2
                    status = 'Not used. Something went wrong';
                case 3
                    status = 'Activation has been completed';
                otherwise
                    error('Something went wrong while checking the status.');
            end
        end
        
        
    end
    
end