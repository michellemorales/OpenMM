% Function to difference each column in a matrix
%
% Description
%  Function to difference each column in a matrix
%
%  This version is a slightly later one than that described in the
%  above published 2013 CSL paper [2]. The algorithm here rather than using binary
%  decision trees using artificial neural networks and combines the
%  features used in the CSL paper with those proposed in Ishi et al.
%  (2008). This updated version has been submitted to CSL for a special
%  issue on glottal source processing on April 14th 2013. It will have
%  reference [1].
%
% Inputs
%  mat  : [samples] [NxM] Feature matrix
%
% Outputs
%  delta_mat : [samples] [NxM] Differenced feature matrix
%
% Example
%  Please see the HOWTO_glottalsource.m example file.
%
% References
%  [1] Drugman, T., Kane, J., Gobl, C., `Automatic Analysis of Creaky
%       Excitation Patterns', Submitted to Computer Speech and
%       Language.
%  [2] Kane, J., Drugman, T., Gobl, C., (2013) `Improved automatic 
%       detection of creak', Computer Speech and Language 27(4), pp.
%       1028-1047.
%  [3] Drugman, T., Kane, J., Gobl, C., (2012) `Resonator-based creaky 
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

function delta_mat = get_delta_mat(mat)

delta_mat=zeros(size(mat));
N=size(mat,2);

for n=1:N
    delta_mat(2:end,n)=diff(mat(:,n));
end
