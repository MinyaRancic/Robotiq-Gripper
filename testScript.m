clear;
clc;

t = timer('TimerFcn', 'data[i] = toby.getCurrent(); i++;', 'StartDelay', .1, 'Period', .1);
toby = RobotiqGripper;
toby.init;
toby.Speed = 255;
toby.Force = 255;
i = 1;
data = zeros(10000);
while true
    toby.Position = 255;
    toby.Position = 0;
    pause(.01);
end