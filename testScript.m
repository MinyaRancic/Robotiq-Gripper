clear;
clc;

current = 0;
%t = timer('TimerFcn', 'current = get(toby, ''Current'');', 'StartDelay', 1, 'Period', 1, 'ExecutionMode', 'FixedRate');
%start(t);
toby = RobotiqGripper;
toby.init;
toby.Speed = 120;
toby.Force = 255;
i = 1;
data = zeros(10000);
while true
    toby.Position = 255;
    fprintf('%d', current);
    toby.Position = 0;
    %pause(.01);
end