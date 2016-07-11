classdef RobotiqGripper < matlab.mixin.SetGet
    % Matlab class to control the robotiq 2-finger gripper
    %   class sends arguments to a python script that controls the gripper
    %   over rs-485 serial. Done this way because matlab does not handle
    %   res-485 serial well.
    %   M. Rancic, 2016
    properties(SetAccess = 'public', GetAccess = 'public')
        Position
        Speed
        Force
        PyControl
        IsInit
    end
    
    methods(Access = 'public')
        function obj = RobotiqGripper

        end
        
        function delete(obj)
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
            obj.Position = int16(0);
            obj.Speed = int16(255);
            obj.Force = int16(255);
        end
    end
    
    methods
        function set.Position(obj, value)
            if(obj.IsInit)
                obj.Position = int16(value);
                obj.PyControl.setPosition(obj.Position);
            else
                error('Must run init() first.')
            end
        end
        
        function set.Speed(obj, value)
            if(obj.IsInit)
                obj.Speed = int16(value);
                obj.PyControl.setSpeed(obj.Speed);
            else
                error('Must run init() first.')
            end
        end
        
        function set.Force(obj, value)
            if(obj.IsInit)
                obj.Force = int16(value);
                obj.PyControl.setForce(obj.Force);
            else
                error('Must run init() first.');
            end
        end
    end
    
end