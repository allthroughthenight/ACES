function [ dpi, dhe, dho, sol, z, rhs1, rhs2, b, cosa ] = FWTCALC( Hnon,Hoverd,unon, nstep, nofour, d, L, deptyp, celdef )
%Calculation of steady waves (on a current) as a Fourier Series

%   Source:  "The Numerical Solution of Steady Water Wave Problems"
%             Computers & Geosciences Vol 14, No 3 pp 357-368, 1988
%            by J.D.Fenton

% INPUTS
% Hnon: wave height
% unon: non dimensionalied mean velocity
% Hoverd: H/d
% L: wave length 
% n: no four
% nstep: the number of steps in Wave Height ramping


% OUTPUTS
% k: wave number 2*pi/L
% z(1, ... 2*n+10): solution vector
% 

    number = 9; % max iteration for each wave height step
    crit = 0.001; % convergence criterion.  If sum of magnitudes of corrections is < crit, the iteration stops
    num = 2*nofour+10; % initialize
    np = 61;
    assert(num<np,'Error: Too many terms in Fourier series');
    dpi = 4/atan(1);
    dhe = Hnon /nstep;
    dho = Hoverd / nstep;
    
    for ns = 1:nstep
        Hnon = ns * dhe;
        Hoverd = ns * dho;
        if ns<=1  %calculate initial linear solution
          [ sol, z, cosa, sina ] = FWTSOL( dpi, Hoverd, Hnon, unon, number, num, nofour, deptyp, celdef );
        else % extrapolate for next wave height 
            for i = 1:num
                z(i) = 2*sol(i,2) - sol(i,1);
            end
        end
        for iter = 1:number 
        % Calculate right sides of equations and differentiate numerically to obtain Jacobian matrix:
            [ rhs1 ] = FWTEQNS( d, L, z, Hoverd, nofour, Hnon, dpi, celdef, unon, cosa, sina );
            for i = 1: num
                h = 0.01*z(i);
                if abs(z(i))<crit
                    h = 10^-5;
                end
                    z(i) = z(i) + h;
                    [ rhs2 ] = FWTEQNS( d, L, z, Hoverd, nofour, Hnon, dpi, celdef, unon, cosa, sina );
                    z(i) = z(i) - h;
                    b(i) = -rhs1(i);
                    for j = 1:num
                        a(j,i) = (rhs2(j) - rhs1(j)) / h;
                    end
            end
            % Solve matrix equation and correct variables using LINPACK routines
% Solve the matrix equation [a(i,j)][correction vector] = [b(i)]
% dgefa factors a double precision matrix by gaussian elimination. 
%call dgefa(a, np, num, ipvt, info)
        [ a, ipvt, info ] = zgefa ( a, np, nofour );
   % *    assert(info~=0, 'ERROR:  Matrix singular')
        %call dgesl(a, np, num, ipvt, b, 0)
        % The b(i) are now the corrections to each variable
        b = dgesl ( a, np, nofour, ipvt, b, 0 );
        sum = 0;
        for i = 1:num
            sum =  sum + abs(b(i));
            z(i) = z(i) + b(i);
        end
        criter = crit;
        if ns == nstep
            criter = 0.01*crit;
        end 
  %*      assert(sum>=criter, 'ERROR: Did not converge after iterations')
        end
        if ns==1
            for i = 1:num
            sol(i,2) = z(i);
            end
        else
            for i = 1:num
                sol(i,1) = sol(i,2);
                sol(i,2) = z(i);
            end
        end
    end
       

    
% 
% k = 2*pi/L;
% 
% z(1) = k*d;
% z(2) = k*Hnon; 
% z(3) = T*sqrt(g*k);
% z(4) = c*sqrt(k/g);
% z(5) = unon*sqrt(g*H)/sqrt(k/g); % for eularian
% z(6) = unon*sqrt(g*H)/sqrt(k/g); % for stokes
% z(7) = ubar*sqrt(k/g);
% z(8) = q*sqrt((k^3)/g);
% z(9) = r*k/g;
% for i= 0:(n+10)
%     z(i+10) = k*eta(i+1);
% end 
% for j=11:(num-N)
%     z(N+j) = B(j-10);
% end

    




end

