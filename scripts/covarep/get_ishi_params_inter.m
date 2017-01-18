% Function to derive parameters used for creaky voice detection in Ishi et
% al (2008) The glottal synchronous parameters (i.e. PwP and IPS) are resampled to a
% fixed update rate.
%
% Description
%  Function to derive parameters used for creaky voice detection in Ishi et
% al (2008) The glottal synchronous parameters (i.e. PwP and IPS) are resampled to a
% fixed update rate.
%
%
% Inputs
%  x        : [samples] [Nx1]  Speech signal
%  fs       : [Hz]      [1x1]  Sampling frequency
%
% Outputs
%  PwP      : [struct]  [Nx1] Struct containing .rise and .fall power peak
%                            parameters
%  IFP      : [samples] [Nx1] Intra-frame periodicity contour
%  IPS      : [samples] [Nx1] Inter-pulse similarity contour
%  bin_dec  : [binary]  [Nx1] Binary creaky voice decision
%
% Example
%  Please see the HOWTO_glottalsource.m example file.
%
% References
%  [1] Ishi, C., Sakakibara, K-I, Ishiguro, H., (2008) `A method for 
%       automatic detection of vocal fry', IEEE TASLP, 16(1), 47-56.
%  [2] Drugman, T., Kane, J., Gobl, C., `Automatic Analysis of Creaky
%       Excitation Patterns', Submitted to Computer Speech and
%       Language.
%  [3] Kane, J., Drugman, T., Gobl, C., (2013) `Improved automatic 
%       detection of creak', Computer Speech and Language 27(4), pp.
%       1028-1047.
%  [4] Drugman, T., Kane, J., Gobl, C., (2012) `Resonator-based creaky 
%       voice detection', Interspeech 2012, Portland, Oregon, USA.
%
% Copyright (c) 2013 University of Mons, FNRS & 2013 Trinity College Dublin
%
% License
%  This code is a part of the GLOAT toolbox with the following
%  licence:
%  This program is free software: you can redistribute it and/or modify
%  it under the terms of the GNU General Public License as published by
%  the Free Software Foundation, either version 3 of the License, or
%  (at your option) any later version.
%  This program is distributed in the hope that it will be useful,
%  but WITHOUT ANY WARRANTY; without even the implied warranty of
%  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%  GNU General Public License for more details.
%
% This function is part of the Covarep project: http://covarep.github.io/covarep
% 
% Authors
%  Thomas Drugman <thomas.drugman@umons.ac.be> & John Kane <kanejo@tcd.ie>

function [PwP,IFP,IPS,bin_dec,dec_orig,IPS_cur,time] = get_ishi_params_inter(x,fs)

% Function to derive acoustics features used in Ishi et al. (2008). The
% glottal synchronous parameters (i.e. PwP and IPS) are resampled to a
% fixed update rate.
%
% REFERENCE:
%       Ishi, C., Sakakibara, K-I, Ishiguro, H., (2008) `A method for 
%       automatic detection of vocal fry', IEEE TASLP, 16(1), 47-56.

%% Initial settings
% Thresholds from Ishi et al (2008)
PwP_thresh=7;
IFP_thresh=0.5;
IPS_thresh=0.5;
maxLen=35/1000*fs;

% Allocate space
IPS=zeros(1,length(x));
PwP.rise=zeros(1,length(x));
PwP.fall=zeros(1,length(x));

%% Extract parameters
[dec_orig,t_IFP,IFP_cur,PwP_cur,IPS_cur,t_pow] = ishi_creak_detection(x,fs,0);
time=[];
%% Resample
if isempty(IFP_cur) || length(IFP_cur) < 3
    IFP=zeros(1,length(x));
else
    IFP=interp1(t_IFP,IFP_cur,1:length(x));
    IFP(isnan(IFP))=0;
end

if isempty(PwP_cur.rise)==0 && length(PwP_cur.rise) > 2
    
    time=round(t_pow(PwP_cur.idx));
    
    for n=1:length(x)
        
        % Find nearest value
        time_cur=time;
        time_cur(time_cur<n)=0;
        [minDist,idx]=min(abs(time_cur-n));
        
        if minDist < maxLen
            PwP.rise(n)=PwP_cur.rise(idx);
            PwP.fall(n)=PwP_cur.fall(idx);
            IPS(n)=IPS_cur(idx);
        end
    end
           
end

%% Generate binary decision
bin_dec=zeros(1,length(x));
bin_dec(PwP.rise>PwP_thresh&IFP<=IFP_thresh&IPS>=IPS_thresh)=1;
        
        