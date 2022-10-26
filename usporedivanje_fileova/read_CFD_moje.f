      subroutine read_CFD_results(lumsurface,nodemap,x,u,
     &              CFDresults_field)

      implicit none

      include   'cdata.h'
      include   'sdata.h'
      include   'mesh_parameters.h'
      include   'user_model_options.h'
      include   'ilt_num_method_parameters.h'
      include   'iofile.h'
      include   'FSG_parameters.h'

      integer   nodemap(9,nnt,nnz,nnr), stlnodes(nnt,nnz), num_lines,
     &          line_number, i,j,k,l, nd, nl, k1,k2,k3, nd1,nd2,nd3,
     &          point_counter, tawss_line_number, osi_line_number,
     &          ecap_line_number
      real*8    lumsurface(nnt,nnz,2), x(ndm,numnp), u(ndf,numnp),
     &          CFDresults_field(nnt,nnz,3), CFDfiles(6,5000),
     &          distance, xx,yy,zz, xl,yl,zl, smallest_distance,
     &          coor(3), value, layer_averaged_result(3),
     &          layer_sum_result(3), zz_down,zz_up, zz1,zz2,zz3,
     &          interpolation_points(2,2), up_dist, down_dist,
     &          z1, z2, t1, t2, linear_interpolation, int_tawss,
     &          int_osi, int_ecap



      logical   waiting, exist_ecap, exist_osi, exist_tawss,
     &          exist_kordinate, reading, pcomp
      character line*80, num*3

      real(kind=8), parameter :: zero=0d0, one=1d0, two=2d0

c=======================================================================


c     Chech for results files
      waiting = .true.
       do while (waiting)

         inquire(file='ECAP',exist=exist_ecap)
         inquire(file='OSI',exist=exist_osi)
         inquire(file='TAWSS',exist=exist_tawss)
         inquire(file='kordinate',exist=exist_kordinate)

         ! ako ne postoje ispisi CFDerrorA

       if (exist_ecap.and.exist_osi.and.
     & exist_tawss.and.exist_kordinate) then
           waiting = .false.
         else
           write(*,*)
           if (.not.exist_ecap) then
             write(*,1000)
             waiting = .true.
           endif
           if (.not.exist_osi) then
             write(*,1001)
             waiting = .true.
           endif
           if (.not.exist_tawss) then
             write(*,1002)
             waiting = .true.
           endif
           if (.not.exist_kordinate) then
             write(*,1003)
             waiting = .true.
           endif
           open(54,file='CFDerrorA',status='replace',action='write',
     &      form='formatted')
           close(54)
           write(*,1015)
         endif

         if (waiting) then
           call sleep(10)
         endif

       enddo

c     Open results files
       open(50,file='koordinate',status='old',action='read',
     &     form='formatted')
       open(51,file='TAWSS',status='old',action='read',
     &     form='formatted')
       open(52,file='OSI',status='old',action='read',
     &     form='formatted')
       open(53,file='ECAP',status='old',action='read',
     &     form='formatted')
       rewind(50)
       rewind(51)
       rewind(52)
       rewind(53)









c     Read results files
       if (luminal_surface_flag.ge.10.and.
     &  luminal_surface_flag.le.15)then


             ! Read "koordinate" file
             reading = .true.
             line_number = -1
             do while (reading)
               read(50,'(a80)') line
               if (pcomp(line(1:2),'(',1)) then
                 line_number = line_number + 1
               endif
               ! End of results
               if (pcomp(line(1:2),')',1)) then
                 reading = .false.
                 exit
               endif
               ! Lines with results
               if (line_number.ge.1) then
                 ! Find ")" in line
                 do nl = 50,2,-1
                   if (line(nl:nl).eq.')') go to 10
                 enddo
                 ! Convert string to real values
10		          call vinput(line(2:nl-1),nl-2,coor,3)
                 ! Save values to the filed
                 CFDfiles(1,line_number) = coor(1)
                 CFDfiles(2,line_number) = coor(2)
                 CFDfiles(3,line_number) = coor(3)
               endif
             enddo


             ! Read "TAWSS" file
             reading = .true.
             tawss_line_number = -1
             line_number = 0
             do while (reading)
               read(51,'(a80)') line
               if (pcomp(line(1:2),'(',1)) then
                 tawss_line_number = tawss_line_number + 1
               endif
               ! End of results
               if (pcomp(line(1:2),')',1)) then
                 reading = .false.
                 exit
               endif
               ! Lines with results
               if (tawss_line_number.ge.1) then
                 ! Convert string to real and save value
                 call vinput(line(1:20),20,value,1)
                 line_number = line_number + 1
                 CFDfiles(4,line_number) = value
               endif
               if (tawss_line_number.eq.0) then
                 tawss_line_number = tawss_line_number + 1
               endif
             enddo


             ! Read "OSI" file
             reading = .true.
             osi_line_number = -1
             line_number = 0
             do while (reading)
               read(51,'(a80)') line
               if (pcomp(line(1:2),'(',1)) then
                 osi_line_number = osi_line_number + 1
               endif
               ! End of results
               if (pcomp(line(1:2),')',1)) then
                 reading = .false.
                 exit
               endif
               ! Lines with results
               if (osi_line_number.ge.1) then
                 ! Convert string to real and save value
                 call vinput(line(1:20),20,value,1)
                 line_number = line_number + 1
                 CFDfiles(5,line_number) = value
               endif
               if (osi_line_number.eq.0) then
                 osi_line_number = osi_line_number + 1
               endif
             enddo


             ! Read "ECAP" file
             reading = .true.
             ecap_line_number = -1
             line_number = 0
             do while (reading)
               read(53,'(a80)') line
               if (pcomp(line(1:2),'(',1)) then
                 ecap_line_number = ecap_line_number + 1
               endif
               ! End of results
               if (pcomp(line(1:2),')',1)) then
                 reading = .false.
                 exit
               endif
               ! Lines with results
               if (ecap_line_number.ge.1) then
                 ! Convert string to real and save value
                 call vinput(line(1:20),20,value,1)
                 line_number = line_number + 1
                 CFDfiles(6,line_number) = value
               endif
               if (ecap_line_number.eq.0) then
                 ecap_line_number = ecap_line_number + 1
               endif
             enddo




  ! Find and write results for lumen nodes for option #1 and #2
         if (luminal_surface_flag.eq.10.or.
     &      luminal_surface_flag.eq.11) then
            num_lines = line_number
            do i = 1,nnt
              do j = 1,nnz
                do k = 1,nnr
                  if (nodemap(1,i,j,k).eq.0) then
                    exit
                  endif
                enddo
                k = k-1
                nd = nodemap(1,i,j,k)
                stlnodes(i,j) = nd

                ! Node coordinates
                xx = x(1,nd) + u(1,nd)
                yy = x(2,nd) + u(2,nd)
                zz = x(3,nd) + u(3,nd)

                ! Loop over "koordinate" file to find closest result node
                smallest_distance = 1000
                line_number = 0
                do l = 1,num_lines
                  ! Coordinates of CFD result node
                  xl = CFDfiles(1,l) * 1000
                  yl = CFDfiles(2,l) * 1000
                  zl = CFDfiles(3,l) * 1000 + translate_distance
                  distance = dsqrt((xx-xl)**2 + (yy-yl)**2 + (zz-zl)**2)
                  if (distance.lt.smallest_distance) then
                    smallest_distance = distance
                    line_number = l
                  endif
                enddo

                ! Save result values for current node
                if (smallest_distance.le.5) then
                  CFDresults_field(i,j,1) = CFDfiles(4,line_number) ! TAWSS
                  CFDresults_field(i,j,2) = CFDfiles(5,line_number)  ! OSI
                  CFDresults_field(i,j,3) = CFDfiles(6,line_number)  ! ECAP
                else
                  CFDresults_field(i,j,1) = 100  ! TAWSS
                  CFDresults_field(i,j,2) = 100  ! OSI
                  CFDresults_field(i,j,3) = 100  ! ECAP
                endif

              enddo
            enddo

  ! Option #3 - circumferential averaging of the results
      elseif (luminal_surface_flag.eq.12.or.
     &          luminal_surface_flag.eq.13) then
        num_lines = line_number
        do j = 2,nnz-1
          do k1 = 1,nnr
            if (nodemap(1,1,j-1,k1).eq.0) then
              exit
            endif
          enddo
          do k2 = 1,nnr
            if (nodemap(1,1,j,k2).eq.0) then
              exit
            endif
          enddo
          do k3 = 1,nnr
            if (nodemap(1,1,j+1,k3).eq.0) then
              exit
            endif
          enddo
          k1 = k1-1
          k2 = k2-1
          k3 = k3-1
          nd1 = nodemap(1,1,j-1,k1)
          nd2 = nodemap(1,1,j,k2)
          nd3 = nodemap(1,1,j+1,k3)

          ! Node z coordinates
          zz1 = x(3,nd1) + u(3,nd1)
          zz2 = x(3,nd2) + u(3,nd2)
          zz3 = x(3,nd3) + u(3,nd3)

          ! Layer boundaries for circumferential averaging
          zz_down = 0.5 * (zz1+zz2)
          zz_up   = 0.5 * (zz2+zz3)
          zz_down = zz_down - 0.75
          zz_up   = zz_up   + 0.75

  ! Loop over "koordinate" file to find nodes in the layer and average them
          layer_sum_result(1:3) = zero
          point_counter = 0
          do l = 1,num_lines
            zl = CFDfiles(3,l) * 1000 + translate_distance
            if (zl.ge.zz_down.and.zl.le.zz_up) then
              layer_sum_result(1) = layer_sum_result(1) +CFDfiles(4,l)
              layer_sum_result(2) = layer_sum_result(2) +CFDfiles(5,l)
              layer_sum_result(3) = layer_sum_result(3) +CFDfiles(6,l)
              point_counter = point_counter + 1
            endif
          enddo
          if (point_counter.eq.0) then
            layer_averaged_result(1:3) = 100
          else
            do k=1,3
            layer_averaged_result(k)=layer_sum_result(k)/point_counter
            enddo
          endif

          ! Save result values for current node
          CFDresults_field(1:nnt,j,1) = layer_averaged_result(1)  ! TAWSS
          CFDresults_field(1:nnt,j,2) = layer_averaged_result(2)  ! OSI
          CFDresults_field(1:nnt,j,3) = layer_averaged_result(3) ! ECAP

        enddo

        CFDresults_field(1:nnt,1,1)   = 100
        CFDresults_field(1:nnt,1,2)   = 100
        CFDresults_field(1:nnt,1,3)   = 100
        CFDresults_field(1:nnt,nnz,1) = 100
        CFDresults_field(1:nnt,nnz,2) = 100
        CFDresults_field(1:nnt,nnz,3) = 100

      endif ! Options



        ! Axisymmetric CFD analysis
        elseif (luminal_surface_flag.eq.14.or.
     &          luminal_surface_flag.eq.15) then
          num_lines = line_number
          do j = 2,nnz-1
            ! Z coordinate of luminal node
             do k = 1,nnr
              if (nodemap(1,1,j,k).eq.0) then
                exit
              endif
            enddo
            k = k-1
            nd = nodemap(1,1,j,k)
            zz = x(3,nd) + u(3,nd)

    ! Loop over "koordinate" file to find closest upper and lower point
            interpolation_points(1:2,1:2) = zero
            down_dist = 1000
            do l = 1,num_lines
              zl = CFDfiles(3,l) * 1000
              if (zl.le.zz.and.(zz-zl).lt.down_dist) then
                down_dist = zz - zl
                interpolation_points(1,1) = zl
                interpolation_points(1,2) = CFDfiles(4,l)
              endif
            enddo
            up_dist = 1000
            do l = 1,num_lines
              zl = CFDfiles(3,l) * 1000
              if (zl.ge.zz.and.(zl-zz).lt.up_dist) then
                up_dist = zl - zz
                interpolation_points(2,1) = zl
                interpolation_points(2,2) = CFDfiles(4,l)
              endif
            enddo

            if (down_dist.eq.1000.or.up_dist.eq.1000) then
              int_tawss = 100
            else
              z1 = interpolation_points(1,1)
              t1 = interpolation_points(1,2)
              z2 = interpolation_points(2,1)
              t2 = interpolation_points(2,2)
              int_tawss = linear_interpolation(z1,z2,t1,t2,zz)
            endif

             ! Save result values for current node
            CFDresults_field(1:nnt,j,1) = int_tawss
c            CFDresults_field(1:nnt,j,2) = int_osi
c            CFDresults_field(1:nnt,j,3) = int_ecap

           enddo

           CFDresults_field(1:nnt,1,1)   = 100
           CFDresults_field(1:nnt,nnz,1) = 100

         endif ! Options

        endif

c  		   Close and delete results files
           close(50,status='delete')
           close(51,status='delete')
           close(52,status='delete')
           close(53,status='delete')


c  		   Open file for writing feap CFD values
           if (modfeap_number.eq.1) then
             open(55,file='CFD_values_feap', status='replace',
     &          action='write', form='formatted')
              write(55,1005)
              write(55,1013)
            else
              open(55,file='CFD_values_feap', status='old',
     &          action='write', form='formatted')
            endif

            ! Write values to TAWSS_values_FEAP file
            write(55,1006) modfeap_number
            write(55,1009,advance='no')
            do k = 1,nnt
              write(55,1010,advance='no') k
            enddo
            write(55,1011,advance='no')
            do k = 1,nnt
              write(55,1012,advance='no')
            enddo
            write(55,*)
            do i = 1,nnz
              write(55,1008,advance='no') i
              do k = 1,nnt
                write(55,1007,advance='no') CFDresults_field(k,i,1)
              enddo
              write(55,*)
              write(55,1014,advance='no')
              do k = 1,nnt
                write(55,1007,advance='no') CFDresults_field(k,i,2)
              enddo
              write(55,*)
              write(55,1014,advance='no')
              do k = 1,nnt
                write(55,1007,advance='no') CFDresults_field(k,i,3)
              enddo
              write(55,*)
              write(55,1014,advance='yes')
            enddo
            write(55,*)
            close(55)

            write(*,1004)

c-----------------------------------------------------------------------
1000  format(' "ECAP" file does not exist! Waiting for file ...')
1001  format(' "OSI" file does not exist! Waiting for file ...')
1002  format(' "TAWSS" file does not exist! Waiting for file ...')
1003  format(' "koordinate" file does not exist! Waiting for file ...')
1004  format(' CFD results files read. ')
1005  format(//1x 'CFD in lumen noded - interpolated from CFD
     & results')
1006  format(/1x 'CFD analysis number', i3 /)
1007  format(f8.3)
1008  format(i7,' |')
1009  format(9x)
1010  format(i8)
1011  format(/8x '-')
1012  format('--------')
1013  format(/3x 'o--->            TAWSS' /
     &        3x '|  theta           OSI' /
     &        3x 'v z               ECAP' /)
1014  format(7x,' |') 1015  format(1x,'"CFDerrorA" file generated!')
1015  format(1x,'"CFDerrorA" file generated!')
c=======================================================================
      end subroutine