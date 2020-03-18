%% Initial Psychtoolbox
%-------------------------------------------------------------------------%
%                         Initialize Psychtoolbox                         %
%-------------------------------------------------------------------------%
% Clear the workspace and the screen
sca;
close all;
clc;
clearvars;

Screen('Preference', 'SkipSyncTests', 1);

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

% Set up alpha-blending for smooth (anti-aliased) lines
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

%% Setting up all properties for every box. (e.i. imageTexture, rects, rectPositions)
%-------------------------------------------------------------------------%
%                          Initialize Variables                           %
%-------------------------------------------------------------------------%
% Screen X, Y positions of seven rectangles. 
squareXpos = [round(screenXpixels*0.1)   round(screenXpixels*0.9)...   
              round(screenXpixels*0.5)   round(screenXpixels*0.5)];   
              % round(screenXpixels*0.35)  round(screenXpixels*0.65)   xCenter];
squareYpos = [round(screenYpixels*0.5)   round(screenYpixels*0.5)...   
              round(screenYpixels*0.1)   round(screenYpixels*0.9)];
              % round(screenYpixels*0.45)  round(screenYpixels*0.45)   round(screenYpixels*0.65)];
numSqaures = length(squareXpos);

box_files = ["Left.png" "Right.png" "Up.png" "Down.png"];  
theImageLocation = [];
imageTextures  = [];
for i = 1:length(box_files)
    theImageLocation{i} = strcat(pwd, '\Pictures\', box_files(i));
    imageTextures{i} = Screen('MakeTexture', window, imread(theImageLocation{i}));
end

rects = nan(4, length(box_files));
rectSize = [0 0 220 220];
for i = 1:length(box_files)
    rects(:, i) = CenterRectOnPointd(rectSize, squareXpos(i), squareYpos(i)); 
end

%% Prior set up for monitors flickering
ifi = Screen('GetFlipInterval', window);

vbl = Screen('Flip', window);
waitframes = 1;

topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);
time = 0;

%% Initialize TCP client
% Communication with TCP client
% t = tcpip('127.0.0.1', 8055);
% disp('Waiting for connection');
% fopen(t);
% disp('Connection OK');

%% Other necessary properties for the stimulation.
%-------------------------------------------------------------------------%
%                   Experiment Set Up (Able to config)                    %
%-------------------------------------------------------------------------%
% Scenario Setup
intensityStep = 10;

% Struct setting nRound, Condition, Frequency
nRound = [1 1 1 1];
cond = [1 1 1 1];
freq = [5.45 6.67 7.5 8.57];
sampling_time = 1; % Sampling time for acquiring data from S1 in every 1 second

% Set the colors to Grey at 75 luminance, White at 255 luminance (max)
fasterBoxColor = [150; 150; 150];
SlowerBoxColor = [255; 255; 255];
CenterColor = [240; 240; 240];
blackColors = [0; 0; 0];

previous_class = 0;

%% Main Function
%-------------------------------------------------------------------------%
%                           Start Experiment                              %
%-------------------------------------------------------------------------%

while ~KbCheck
    
%     if (time >= sampling_time)
%         % Get data from classifier on simulink
%         data = fread(t, [1, t.BytesAvailable]);
%         if ~eq(data, NaN)
%             class = char(data);
%             
%             if isequal(eq(class, '6'), eq(previous_class, class))
%                 %LeftColor = min(LeftColor + intensityStep, 255);   % Can increase intensity up to 255
%                 disp ('intensity increase');
%             elseif isequal(eq(class, '7.5'), eq(previous_class, class))
%                 %RightColor = max(RightColor - intensityStep, 0);   % Can decrease to 0 (minimum intensity) 
%                 disp ('intensity decrease');
%             elseif isequal(eq(previous_class, '6'), ~eq(previous_class, class))
%                 %RightColor = LeftColor;
%                 disp ('eiei');
%             elseif isequal(eq(previous_class, '7.5'), ~eq(previous_class, class))
%                 %LeftColor = RightColor;
%                 disp ('eiei2');
%             end    
%             previous_class = class;
%             sampling_time = sampling_time + 1;
%         end
%     end
    
    for i = 1:length(box_files)
        [next_nRound, next_boxCond] = Flickering_box(imageTextures{i}, window, freq(i), nRound(i), cond(i), time, rects(:, i));  
        nRound(i) = next_nRound;
        cond(i) = next_boxCond;
    end    
    
    Screen('Flip', window);
    time = time + ifi;
end

% Clear the screen
KbStrokeWait;
sca;
% fclose(t);
clear t
clear all

%% Handled all functions
%-------------------------------------------------------------------------%
%                         Function initialization                         %
%-------------------------------------------------------------------------%
function [next_nRound, next_boxCond] = Flickering_box(imgTexture, window, frequency, nRound, boxCond, time, rect)
    if (time >= nRound/(frequency*2))
        boxCond = ~boxCond;
        nRound = nRound + 1;
    end
    
    if boxCond
        Screen('DrawTexture', window, imgTexture, [], rect, [], [], 1);
    else 
        Screen('DrawTexture', window, imgTexture, [], rect, [], [], 0);
    end
    
    next_nRound = nRound;
    next_boxCond = boxCond;
end