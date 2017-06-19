function [ ubig, wbig, ax, ay, pbig, eta ] = FWTKIN( xoverl, y, dpi, n, k, d,  z, ft, deptyp, g, rho )
%Determine velocity, pressure, & acceleration at(kx,ky),and water surface elevation at (kx):

% Determine water surface elevation (k*eta)
    kx   = 2.*dpi*xoverl;
    ky   = k * y;
    kd   = k * d;
    keta = 0.5 * ft(n) * cos(n*kx);
    for j=1:n-1
        keta  = keta + ft(j)*cos(j*kx);
    end
    
    eta = real(keta/k);
% Check to see if (kx,ky) outside of wave domain:
    if ky > keta || ky < -kd
       fprint('ERROR: (X/L,Z) pair not in wave domain') 
       ubig = 0; 
       wbig = 0;
       pbig = 0;
       ax = 0; 
       ay = 0;
    end
      u   = - z(7);
      v   = 0;
      ux  = 0;
      uy  = 0;
      
    if deptyp==2
        for j = 1:n
            e  = exp(j*(z(1)+ky));
            s  = .5 * (e-1/e);
            c  = .5 * (e+1/e);
            b  = z(n+j+10) / cosh(j*z(1));
            cx = cos(j*kx);
            sx = sin(j*kx);
            u  = u  + j*b*c*cx;
            v  = v  + j*b*s*sx;
            ux = ux + j*j*b*c*sx;
            uy = uy + j*j*b*s*cx;
        end
    else
        for j = 1:n
            e  = exp(j*ky);
            cx = cos(j*kx);
            sx = sin(j*kx);
            u  = u  + j*z(n+j+10)*e*cx;
            v  = v  + j*z(n+j+10)*e*sx;
            ux = ux + j*j*z(n+j+10)*e*sx;
            uy = uy + j*j*z(n+j+10)*e*cx;
        end
    end
    
    press = z(9) - ky - 0.5*( u^2 + v^2);

      u     = u * sqrt(g/k);
      v     = v * sqrt(g/k);
      ux    = -sqrt(g*k) * ux;
      uy    =  sqrt(g*k) * uy;

      ubig  = real( u + z(4)*sqrt(g/k) );
      wbig  = real( v );
      pbig  = real( (rho*g/k) * press );
      ax    = real( u*ux + v*uy );
      ay    = real( u*uy - v*ux );

end

