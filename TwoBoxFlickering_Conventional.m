%-------------------------------------------------------------------------%
%                               Initialize                                %
%-------------------------------------------------------------------------%
% Clear the workspace and the screen
sca;
close all;
clearvars;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');

% Draw to the external screen if avaliable
screenNumber = max(screens);

% Define black and white
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect of 200 by 200 pixels
baseRect = [0 0 270 270];

% Screen X positions of our three rectangles
squareXpos = [round(screenXpixels * 0.25) round(screenXpixels * 0.75)];
numSqaures = length(squareXpos);

% Make our rectangle coordinates
allRects = nan(4, 2);
for i = 1:numSqaures
    allRects(:, i) = CenterRectOnPointd(baseRect, squareXpos(i), yCenter);
end
ifi = Screen('GetFlipInterval', window);

vbl = Screen('Flip', window);
waitframes = 1;

topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);
time = 0;
nL = 1;
nR = 1;
nC = 1;
conditionL = true;
conditionR = true;

%-------------------------------------------------------------------------%
%                   Experiment Set Up (Able to config)                    %
%-------------------------------------------------------------------------%
% Scenario Setup
frequencyL = 6.0;
frequencyR = 7.5;
intensityStep = 10;

% Set the colors to Grey at 75 luminance, White at 255 luminance (max)
LeftColor = [255; 255; 255];
RightColor = [255; 255; 255];
blackColors = [0; 0; 0];

%-------------------------------------------------------------------------%
%                           Start Experiment                              %
%-------------------------------------------------------------------------%

while ~KbCheck
    %---------------------------------------------------------------------%
    %                     Flikering Condition Change                      %
    %---------------------------------------------------------------------%
    % Change condition(black -> white or white -> black) in every round n
    if (time >= nL/(frequencyL*2))
        conditionL = ~conditionL;
        nL = nL + 1;
    end
    
    if (time >= nR/(frequencyR*2))
        conditionR = ~conditionR;
        nR = nR + 1;
    end
    
    %---------------------------------------------------------------------%
    %                           Draw Animation                            %
    %---------------------------------------------------------------------%
    if conditionL
        Screen('FillRect', window, (LeftColor./255), allRects(:,1));
    else 
        Screen('FillRect', window, blackColors, allRects(:,1));
    end
    
    if conditionR
        Screen('FillRect', window, (RightColor./255), allRects(:,2));
    else 
        Screen('FillRect', window, blackColors, allRects(:,2));
    end
    
    vbl = Screen('Flip', window, vbl + (waitframes - 0.5) * ifi);
    
    time = time + ifi;
end

% Clear the screen
sca;