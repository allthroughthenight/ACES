function [MR,S,MRintc,MRintt,Sintc,Sintt]=WFVW1(d,H,x,L,ww)

N=90;

%Pressure values included hydrostatic pressure
[ycm,ytm,pcm,ptm,mcm,mtm]=WFVW2(N,d,L,H,x,ww,0);

[ycs,yts,pcs,pts,mcs,mts]=WFVW2(N,d,L,H,x,ww,1);

ycrm=ycm(N+1)+d;
ycrs=ycrm;

% Crest at Wall
% Integrate for Miche-Rundgren force value 
[fcrm]=WFVW3(N,ycm,pcm);

% Integrate for Sainflou force value
[fcrs]=WFVW3(N,ycs,pcs);

% Integrate for Miche-Rundgren moment value
[mcrm]=WFVW3(N,ycm,mcm);

% Integrate for Sainfluo moment value
[mcrs]=WFVW3(N,ycs,mcs);

% Trough at Wall
ytrm=ytm(N+1)+d;
ytrs=ytrm;

% Integrate for Miche-Rundgren force value
[ftrm]=WFVW3(N,ytm,ptm);

%Integrate for Sainflou force value
[ftrs]=WFVW3(N,yts,pts);

%Integrate for Miche-Rundgren moment value
[mtrm]=WFVW3(N,ytm,mtm);

%Integrate for Sainfluo moment value
[mtrs]=WFVW3(N,yts,mts);

if fcrm<fcrs && mcrm<mcrs %Equation delivering lowest result should be used in design
    disp('Miche-Rundgren is recommendend for this case.')
else
    disp('Sainflou is recommended for this case.')
end

MR=[ycrm,fcrm,mcrm,ytrm,ftrm,mtrm];
S=[ycrs,fcrs,mcrs,ytrs,ftrs,mtrs];

%Seperates wave pressure and hydrostatic pressure
[hpcm,wpcm]=WFVW4(N,ycm,pcm,ww);

[hptm,wptm]=WFVW4(N,ytm,ptm,ww);

[hpcs,wpcs]=WFVW4(N,ycs,pcs,ww);

[hpts,wpts]=WFVW4(N,yts,pts,ww);

MRintc=[ycm,wpcm,hpcm,pcm,mcm];
MRintt=[ytm,wptm,hptm,ptm,mtm];

Sintc=[ycs,wpcs,hpcs,pcs,mcs];
Sintt=[yts,wpts,hpts,pts,mts];





