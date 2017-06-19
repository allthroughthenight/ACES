function [k, c, L, u1, u2, ubar, q, r, I, Ek, Ep, E, Ub2, Sxx, Ef, Q, R, ft ] = FWTRSLT( z, n, H, g, rho, cosa, deptyp, d )
%Capture general and integral results in appropriate variables:

    % Determine the Fourier coefficients of surface elevation:
    for j = 1:n
        sum = 0.5 * (z(10) + z(n+10)*(-1)^j);
        for m=1:n-1
            sum = sum + z(10+m)*cosa(mod(m*j, n+n)+1);
        end
        ft(j) = 2 * sum/n;
    end
    % Capture dimensional wave properties from solution array:
      k    = z(2) / H;
      c    = z(4) / sqrt(k/g);
      L    = real( c * z(3)/sqrt(k*g) );
      u1   = z(5) / sqrt(k/g);
      u2   = z(6) / sqrt(k/g);
      ubar = z(7) / sqrt(k/g);
      q    = z(8) / sqrt((k^3)/g);
      r    = z(9) * g/k;
    % Determine integral parameters (non-dimensional):
      I = z(8) +z(1) * z(5);
      Ek = 0.5 * (z(4) * I + z(5)*(z(8)-z(7)*z(1)));
      Ep = 0.5 * (z(10)^2 + z(n+10)^2);
      
      for i = 1:n-1
          Ep = Ep + z(10+i)^2;
      end
      Ep = Ep/(2*n);
      Ub2 = 2*z(9) - z(4)^2 + 2*z(5)*z(4);
      
      if deptyp==2
          Q = z(7)*z(1) - z(8);
          R = z(9) + z(1); 
      end 
      % Express Integral parameters as dimensional quantities:
      I = I * rho * sqrt(g/(k^3));
      Ek    = Ek * rho * g / (k^2);
      Ep    = Ep * rho * g / (k^2);
      E = Ep + Ek;
      Ub2   = Ub2 * g / k;
      Sxx   = 4*Ek - 3*Ep + rho*d*Ub2 - 2*u1*I;
      Ef  = (3*Ek - 2*Ep - 2*u1*I)*c + Ub2*(I + rho*c*d)/2;
      Q  = Q / sqrt((k^3)/g);
      R  = R * g / k;
          

end

