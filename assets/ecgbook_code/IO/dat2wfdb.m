function S = WriteSignalToWFDB(data, hea, Fs, recName, baseTime)
% S = dat2wfdb(data, hea, Fs, recName, baseTime);
%
% function to make a WFDB file from a data stream.
% S is the header structure.
%
% Defaults: data = sine wave, recName = 'record';  Fs = 256;
%           leadDesc = 'V5'; baseTime = '00:00:00 01/03/2005';
%
% Gari Clifford gari AT mit DOT edu 2005

% Modified by Shamim Nemati <shamim@mit.edu> to accept a header file with
% proper gain, baseline information.

% hea(i).gain: A/D units (sample) / physical unit (mV)
% hea(i).baseline: sample value correponding to an input of zero in physical unit

if (nargin < 1) t=[1:1:1024*10]/256; data = sin(2*pi*t)*500; data=data'; end
    if (nargin < 2) return; end
    if (nargin < 3) Fs = 256; end
    if (nargin < 4) recName = 'record'; end
    if (nargin < 5) baseTime = '00:00:00 01/08/2008'; end

    [m n]=size(data); % assume data is longer than # channels
    if (m<n) data=data';end
    [m num_ch]=size(data);

    % create header structure
    S = WFDB_Siginfo(n);
    for i=1:num_ch
        data(:,i) = data(:,i)*hea(i).gain + hea(i).baseline;
        S(i).fname = strcat(recName,'.dat');
        S(i).desc = hea(i).desc;
        S(i).units = hea(i).units;
        S(i).gain = hea(i).gain;
        S(i).baseline = hea(i).baseline;
        S(i).initval = hea(i).initval;
        S(i).group = hea(i).group;
        S(i).fmt = hea(i).fmt;
        S(i).sp = hea(i).spf;
        S(i).bsize = hea(i).bsize;
        S(i).adcres = hea(i).adcres;
        S(i).adczero = hea(i).adczero;
    end

    % open file for writing
    WFDB_osigfopen(S);
    % set the intial parameters
    WFDB_setsampfreq(Fs);
    WFDB_setbasetime(baseTime);
    % write the data
    WFDB_putvec(data); % might have to transpose this if > 1D
    % write the header
    WFDB_newheader(recName);
    % clean up
    WFDB_wfdbquit;

