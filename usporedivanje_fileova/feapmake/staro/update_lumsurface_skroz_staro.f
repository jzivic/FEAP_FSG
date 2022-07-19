      subroutine update_lumsurface(lumsurface,nodemap,x,u,
     &              CFDresults_field)

      implicit   none

      include   'ilt_num_method_parameters.h'
      include   'mesh_parameters.h'
      include   'user_model_options.h'
      include   'cdata.h'
      include   'sdata.h'
      include   'num_method_parameters.h'
      include   'FSG_parameters.h'
      
      real*8    lumsurface(nnt,nnz,2), x(ndm,numnp), u(ndf,numnp),
     &          CFDresults_field(nnt,nnz,3), tawss
      integer   nodemap(9,nnt,nnz,nnr)
      
      real*8    R_lumen,zmin,zmax,thmin,thmax,xx,yy,zz,pi,R,theta,
     &          R1,R2,R3,R4, xx1,xx2,xx3,xx4, yy1,yy2,yy3,yy4,
     &          tawss1,tawss2,tawss3,tawss4
      integer   net,nez,nd,i,j,k, a, b, k1,k2,k3,k4, nd1,nd2,nd3,nd4
      logical   moved(nnt,nnz)
      
      real*8,   parameter :: zero=0d0, one=1d0, two=2d0, tol=1d-3
      
      save
c======================================================================
      
c     Define boundaries (for luminal surface flag 5 and 6)
      pi = 4d0*datan(1d0)
      thmin = ilt_theta_min * pi / 180d0
      thmax = ilt_theta_max * pi / 180d0
      zmin = ilt_z_min
      zmax = ilt_z_max
      
c     Define luminal surface up to which elements are added
      if (luminal_surface_flag.le.2) then
        ! lumsurface is defined in initialize_ilt_map.h and it is constant
        
      elseif (luminal_surface_flag.eq.3) then
        R_lumen = lumsurface(1,1,1) + delta_ilt_thickness
        lumsurface(1:nnt,1:nnz,1) = R_lumen
        
      elseif (luminal_surface_flag.eq.4) then
        R_lumen = lumsurface(1,1,1) + delta_ilt_thickness
        lumsurface(2:3,2:3,1) = R_lumen
        
      elseif (luminal_surface_flag.eq.5) then
        do j = 1,nnz
          do i = 1,nnt
            nd = nodemap(1,i,j,1)
            xx = x(1,nd) + u(1,nd)
            yy = x(2,nd) + u(2,nd)
            zz = x(3,nd) + u(3,nd)
            R = dsqrt(xx**two + yy**two)
            if (zz.ge.zmin.and.zz.le.zmax) then
              lumsurface(i,j,1) = lum_surf_radius
            else
              lumsurface(i,j,1) = R
            endif
          enddo
        enddo
        
      elseif (luminal_surface_flag.eq.6) then
        do j = 1,nnz
          do i = 1,nnt
            nd = nodemap(1,i,j,1)
            xx = x(1,nd) + u(1,nd)
            yy = x(2,nd) + u(2,nd)
            zz = x(3,nd) + u(3,nd)
            R = dsqrt(xx**two + yy**two)
            if (yy.ge.(zero-tol)) then
              theta = dacos(xx/R)
            else
              theta = dacos(-one) + dacos(-xx/R)
            endif
            if (zz.ge.zmin.and.zz.le.zmax.and.
     &          theta.ge.thmin.and.theta.le.thmax) then
              lumsurface(i,j,1) = lum_surf_radius
            else
              lumsurface(i,j,1) = R
            endif
          enddo
        enddo
            
      elseif (luminal_surface_flag.eq.7) then
        ! do nothing, testing thrombus adding algorithm
        ! lumsurface is idefined in define_mapadd.f
        
      elseif (luminal_surface_flag.eq.8) then
        ! lumsurface is gradualy chanching
        !  - start -          - every lum_surf_step_time - 
        ! lum_surf_radius -> minus lum_surf_step_dist -> end_lum_surf_radius
        
        if (modfeap_number.eq.1) then
          lumsurface(1:nnt,1:nnz,1) = lum_surf_radius
        endif
        lum_surf_last_time = timestep
        
      elseif (luminal_surface_flag.eq.9) then
        do j = 1,nnz
          do i = 1,nnt
            nd = nodemap(1,i,j,1)
            xx = x(1,nd) + u(1,nd)
            yy = x(2,nd) + u(2,nd)
            zz = x(3,nd) + u(3,nd)
            R = dsqrt(xx**two + yy**two)
            if (yy.ge.(zero-tol)) then
              theta = dacos(xx/R)
            else
              theta = dacos(-one) + dacos(-xx/R)
            endif
            if (zz.ge.zmin.and.zz.le.zmax.and.
     &          theta.ge.thmin.and.theta.le.thmax) then
              lumsurface(i,j,1) = lumsurface(i,j,1) +delta_ilt_thickness
            else
              lumsurface(i,j,1) = R
            endif
          enddo
        enddo
       
c     Update luminal surface based on CFD results
       
      ! Option #1 and #4
      elseif (luminal_surface_flag.eq.10.or.
     &        luminal_surface_flag.eq.13.or.
     &        luminal_surface_flag.eq.15) then
        do j = 1,nnz
          do i = 1,nnt
            ! Get current radius
            do k = 1,nnr
              if (nodemap(1,i,j,k).eq.0) then
                exit
              endif
            enddo
            k = k-1
            nd = nodemap(1,i,j,k)
            xx = x(1,nd) + u(1,nd)
            yy = x(2,nd) + u(2,nd)
            R = dsqrt(xx**two + yy**two)
            ! Get TAWSS
            tawss = CFDresults_field(i,j,1)
            ! Set lumsurface radius
            if (tawss.le.TAWSS_boundary_value) then
              lumsurface(i,j,1) = R - ilt_elem_th * 1.05
            else
              lumsurface(i,j,1) = R
            endif
          enddo
        enddo
      
      ! Option #2 and #3
      elseif (luminal_surface_flag.eq.11.or.
     &        luminal_surface_flag.eq.12.or.
     &        luminal_surface_flag.eq.14) then
        moved(1:nnt,1:nnz) = .false.
        do j = 1,nnz-1
          do i = 1,nnt-1
            ! Get current radii
            do k1 = 1,nnr
              if (nodemap(1,i,j,k1).eq.0) then
                exit
              endif
            enddo
            do k2 = 1,nnr
              if (nodemap(1,i,j+1,k2).eq.0) then
                exit
              endif
            enddo
            do k3 = 1,nnr
              if (nodemap(1,i+1,j+1,k3).eq.0) then
                exit
              endif
            enddo
            do k4 = 1,nnr
              if (nodemap(1,i+1,j,k4).eq.0) then
                exit
              endif
            enddo
            k1 = k1-1
            k2 = k2-1
            k3 = k3-1
            k4 = k4-1
            nd1 = nodemap(1,i,j,k1)
            nd2 = nodemap(1,i,j+1,k2)
            nd3 = nodemap(1,i+1,j+1,k3)
            nd4 = nodemap(1,i+1,j,k4)
            
            xx1 = x(1,nd1) + u(1,nd1)
            yy1 = x(2,nd1) + u(2,nd1)
            R1 = dsqrt(xx1**two + yy1**two)
            xx2 = x(1,nd2) + u(1,nd2)
            yy2 = x(2,nd2) + u(2,nd2)
            R2 = dsqrt(xx2**two + yy2**two)
            xx3 = x(1,nd3) + u(1,nd3)
            yy3 = x(2,nd3) + u(2,nd3)
            R3 = dsqrt(xx3**two + yy3**two)
            xx4 = x(1,nd4) + u(1,nd4)
            yy4 = x(2,nd4) + u(2,nd4)
            R4 = dsqrt(xx4**two + yy4**two)
            
            ! Get TAWSS
            tawss1 = CFDresults_field(i,j,1)
            tawss2 = CFDresults_field(i,j+1,1)
            tawss3 = CFDresults_field(i+1,j+1,1)
            tawss4 = CFDresults_field(i+1,j,1)
            
            ! Set lumsurface radius
            if (tawss1.le.TAWSS_boundary_value.or.
     &          tawss2.le.TAWSS_boundary_value.or.
     &          tawss3.le.TAWSS_boundary_value.or.
     &          tawss4.le.TAWSS_boundary_value) then
              if (.not.moved(i,j)) then
                lumsurface(i,j,1) = R1 - ilt_elem_th * 1.05
                moved(i,j) = .true.
              endif
              if (.not.moved(i,j+1)) then
                lumsurface(i,j+1,1) = R2 - ilt_elem_th * 1.05
                moved(i,j+1) = .true.
              endif
              if (.not.moved(i+1,j+1)) then
                lumsurface(i+1,j+1,1) = R3 - ilt_elem_th * 1.05
                moved(i+1,j+1) = .true.
              endif
              if (.not.moved(i+1,j)) then
                lumsurface(i+1,j,1) = R4 - ilt_elem_th * 1.05
                moved(i+1,j) = .true.
              endif
            else
              if (.not.moved(i,j)) then
                lumsurface(i,j,1) = R1
              endif
              if (.not.moved(i,j+1)) then
                lumsurface(i,j+1,1) = R2
              endif
              if (.not.moved(i+1,j+1)) then
                lumsurface(i+1,j+1,1) = R3
              endif
              if (.not.moved(i+1,j)) then
                lumsurface(i+1,j,1) = R4
              endif
            endif
          enddo
        enddo
      
      endif    
      
c======================================================================      
      end
