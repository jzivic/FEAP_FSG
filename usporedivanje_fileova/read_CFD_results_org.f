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
     &          point_counter
      real*8    lumsurface(nnt,nnz,2), x(ndm,numnp), u(ndf,numnp),
     &          CFDresults_field(nnt,nnz,3), CFDfiles(6,5000),
     &          distance, xx,yy,zz, xl,yl,zl, smallest_distance,
     &          coor(3), value, layer_averaged_result(3),
     &          layer_sum_result(3), zz_down,zz_up, zz1,zz2,zz3
            
      logical   waiting, exist_ecap, exist_osi, exist_tawss, 
     &          exist_kordinate, reading, pcomp
      character line*80
      
      real(kind=8), parameter :: zero=0d0, one=1d0, two=2d0

c=======================================================================

c     Chech for results files
      waiting = .true.
      do while (waiting)
      
        inquire(file='ECAP',exist=exist_ecap)
        inquire(file='OSI',exist=exist_osi)
        inquire(file='TAWSS',exist=exist_tawss)
        inquire(file='kordinate',exist=exist_kordinate)
        
        ! ako ne postoje ispiši CFDerrorA
        
        if (exist_ecap.and.exist_osi.and.exist_tawss.and.
     &      exist_kordinate) then
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
      open(50,file='kordinate',status='old',action='read',
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
      if (luminal_surface_flag.eq.10.or.luminal_surface_flag.eq.11.or.
     &    luminal_surface_flag.eq.12.or.luminal_surface_flag.eq.13) then
      
        ! Read "kordinate" file
          ! Skip lines with no results
          do i = 1,49
            read(50,'(a80)') line
          enddo
          ! Read line with coordinates
          reading = .true.
          line_number = 0
          do while (reading)
            read(50,'(a80)') line
            if (pcomp(line(1:2),')',1)) then
              reading = .false.
              exit
            endif
            ! Find ")" in line
            do nl = 50,2,-1
              if (line(nl:nl).eq.')') go to 10
            enddo
            ! Convert string to real values
10          call vinput(line(2:nl-1),nl-2,coor,3) 
            line_number = line_number + 1
            ! Save values to the filed
            CFDfiles(1,line_number) = coor(1)
            CFDfiles(2,line_number) = coor(2)
            CFDfiles(3,line_number) = coor(3)
          enddo
      
        ! Read "TAWSS" file
          ! Skip lines with no results
          do i = 1,49
            read(51,'(a80)') line
          enddo
          ! Read line with result
          reading = .true.
          line_number = 0
          do while (reading)
            read(51,'(a80)') line
            if (pcomp(line(1:2),')',1)) then
              reading = .false.
              exit
            endif
            ! Convert string to real and save value
            call vinput(line(1:20),20,value,1) 
            line_number = line_number + 1
            CFDfiles(4,line_number) = value
          enddo
      
        ! Read "OSI" file
          ! Skip lines with no results
          do i = 1,49
            read(52,'(a80)') line
          enddo
          ! Read line with result
          reading = .true.
          line_number = 0
          do while (reading)
            read(52,'(a80)') line
            if (pcomp(line(1:2),')',1)) then
              reading = .false.
              exit
            endif
            ! Convert string to real and save value
            call vinput(line(1:20),20,value,1) 
            line_number = line_number + 1
            CFDfiles(5,line_number) = value
          enddo

      
        ! Read "ECAP" file
          ! Skip lines with no results
          do i = 1,49
            read(53,'(a80)') line
          enddo
          ! Read line with result
          reading = .true.
          line_number = 0
          do while (reading)
            read(53,'(a80)') line
            if (pcomp(line(1:2),')',1)) then
              reading = .false.
              exit
            endif
            ! Convert string to real and save value
            call vinput(line(1:20),20,value,1) 
            line_number = line_number + 1
            CFDfiles(6,line_number) = value
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

              ! Loop over "kordinate" file to find closest result node
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
                CFDresults_field(i,j,1) = CFDfiles(4,line_number)  ! TAWSS
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

            ! Loop over "kordinate" file to find nodes in the layer and average them
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
      
      endif
      
c     Close and delete results files
      close(50,status='delete')
      close(51,status='delete')
      close(52,status='delete')
      close(53,status='delete')
      
c     Write values to log file
      write(ilg,1005)
      write(ilg,1013)
      write(ilg,1006) modfeap_number
      write(ilg,1009,advance='no')
      do k = 1,nnt
        write(ilg,1010,advance='no') k
      enddo
      write(ilg,1011,advance='no')
      do k = 1,nnt
        write(ilg,1012,advance='no')
      enddo
      write(ilg,*)
      do i = 1,nnz
        write(ilg,1008,advance='no') i
        do k = 1,nnt
          write(ilg,1007,advance='no') CFDresults_field(k,i,1)
        enddo
        write(ilg,*)
        write(ilg,1014,advance='no')
        do k = 1,nnt
          write(ilg,1007,advance='no') CFDresults_field(k,i,2)
        enddo
        write(ilg,*)
        write(ilg,1014,advance='no')
        do k = 1,nnt
          write(ilg,1007,advance='no') CFDresults_field(k,i,3)
        enddo
        write(ilg,*)
        write(ilg,1014,advance='yes')
      enddo
      write(ilg,*)
      

      write(*,1004)
   
c-----------------------------------------------------------------------
1000  format(' "ECAP" file does not exist! Waiting for file ...')
1001  format(' "OSI" file does not exist! Waiting for file ...')
1002  format(' "TAWSS" file does not exist! Waiting for file ...')
1003  format(' "kordinate" file does not exist! Waiting for file ...')
1004  format(' CFD results files read. ')
1005  format(//1x 'CFD in lumen noded - interpolated from CFD 
     &          results')
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
1014  format(7x,' |')
1015  format(1x,'"CFDerrorA" file generated!')
c=======================================================================      
      end subroutine






c     c STARA VERZIJA SKRIPTE KOJA SADRZI ECAP I OSI FILE
c     c=======================================================================
c
c     c     Chech for results files
c           waiting = .true.
c           do while (waiting)
c
c             inquire(file='ECAP',exist=exist_ecap)
c             inquire(file='OSI',exist=exist_osi)
c             inquire(file='TAWSS',exist=exist_tawss)
c             inquire(file='kordinate',exist=exist_kordinate)
c
c             ! ako ne postoje ispisi CFDerrorA
c
c             if (exist_ecap.and.exist_osi.and.exist_tawss.and.
c          &      exist_kordinate) then
c               waiting = .false.
c             else
c               write(*,*)
c               if (.not.exist_ecap) then
c                 write(*,1000)
c                 waiting = .true.
c               endif
c               if (.not.exist_osi) then
c                 write(*,1001)
c                 waiting = .true.
c               endif
c               if (.not.exist_tawss) then
c                 write(*,1002)
c                 waiting = .true.
c               endif
c               if (.not.exist_kordinate) then
c                 write(*,1003)
c                 waiting = .true.
c               endif
c               open(54,file='CFDerrorA',status='replace',action='write',
c          &      form='formatted')
c               close(54)
c               write(*,1015)
c             endif
c
c             if (waiting) then
c               call sleep(10)
c             endif
c
c           enddo
c
c     c     Open results files
c           open(50,file='kordinate',status='old',action='read',
c          &     form='formatted')
c           open(51,file='TAWSS',status='old',action='read',
c          &     form='formatted')
c           open(52,file='OSI',status='old',action='read',
c          &     form='formatted')
c           open(53,file='ECAP',status='old',action='read',
c          &     form='formatted')
c           rewind(50)
c           rewind(51)
c           rewind(52)
c           rewind(53)
c
c     c     Read results files
c           if (luminal_surface_flag.eq.10.or.luminal_surface_flag.eq.11.or.
c          &    luminal_surface_flag.eq.12.or.luminal_surface_flag.eq.13) then
c
c             ! Read "kordinate" file
c               ! Skip lines with no results
c               do i = 1,49
c                 read(50,'(a80)') line
c               enddo
c               ! Read line with coordinates
c               reading = .true.
c               line_number = 0
c               do while (reading)
c                 read(50,'(a80)') line
c                 if (pcomp(line(1:2),')',1)) then
c                   reading = .false.
c                   exit
c                 endif
c                 ! Find ")" in line
c                 do nl = 50,2,-1
c                   if (line(nl:nl).eq.')') go to 10
c                 enddo
c                 ! Convert string to real values
c     10          call vinput(line(2:nl-1),nl-2,coor,3)
c                 line_number = line_number + 1
c                 ! Save values to the filed
c                 CFDfiles(1,line_number) = coor(1)
c                 CFDfiles(2,line_number) = coor(2)
c                 CFDfiles(3,line_number) = coor(3)
c               enddo
c
c             ! Read "TAWSS" file
c               ! Skip lines with no results
c               do i = 1,49
c                 read(51,'(a80)') line
c               enddo
c               ! Read line with result
c               reading = .true.
c               line_number = 0
c               do while (reading)
c                 read(51,'(a80)') line
c                 if (pcomp(line(1:2),')',1)) then
c                   reading = .false.
c                   exit
c                 endif
c                 ! Convert string to real and save value
c                 call vinput(line(1:20),20,value,1)
c                 line_number = line_number + 1
c                 CFDfiles(4,line_number) = value
c               enddo
c
c             ! Read "OSI" file
c               ! Skip lines with no results
c               do i = 1,49
c                 read(52,'(a80)') line
c               enddo
c               ! Read line with result
c               reading = .true.
c               line_number = 0
c               do while (reading)
c                 read(52,'(a80)') line
c                 if (pcomp(line(1:2),')',1)) then
c                   reading = .false.
c                   exit
c                 endif
c                 ! Convert string to real and save value
c                 call vinput(line(1:20),20,value,1)
c                 line_number = line_number + 1
c                 CFDfiles(5,line_number) = value
c               enddo
c
c
c             ! Read "ECAP" file
c               ! Skip lines with no results
c               do i = 1,49
c                 read(53,'(a80)') line
c               enddo
c               ! Read line with result
c               reading = .true.
c               line_number = 0
c               do while (reading)
c                 read(53,'(a80)') line
c                 if (pcomp(line(1:2),')',1)) then
c                   reading = .false.
c                   exit
c                 endif
c                 ! Convert string to real and save value
c                 call vinput(line(1:20),20,value,1)
c                 line_number = line_number + 1
c                 CFDfiles(6,line_number) = value
c               enddo
c
c
c             ! Find and write results for lumen nodes for option #1 and #2
c             if (luminal_surface_flag.eq.10.or.
c          &      luminal_surface_flag.eq.11) then
c               num_lines = line_number
c               do i = 1,nnt
c                 do j = 1,nnz
c                   do k = 1,nnr
c                     if (nodemap(1,i,j,k).eq.0) then
c                       exit
c                     endif
c                   enddo
c                   k = k-1
c                   nd = nodemap(1,i,j,k)
c                   stlnodes(i,j) = nd
c
c                   ! Node coordinates
c                   xx = x(1,nd) + u(1,nd)
c                   yy = x(2,nd) + u(2,nd)
c                   zz = x(3,nd) + u(3,nd)
c
c                   ! Loop over "kordinate" file to find closest result node
c                   smallest_distance = 1000
c                   line_number = 0
c                   do l = 1,num_lines
c                     ! Coordinates of CFD result node
c                     xl = CFDfiles(1,l) * 1000
c                     yl = CFDfiles(2,l) * 1000
c                     zl = CFDfiles(3,l) * 1000 + translate_distance
c                     distance = dsqrt((xx-xl)**2 + (yy-yl)**2 + (zz-zl)**2)
c                     if (distance.lt.smallest_distance) then
c                       smallest_distance = distance
c                       line_number = l
c                     endif
c                   enddo
c
c                   ! Save result values for current node
c                   if (smallest_distance.le.5) then
c                     CFDresults_field(i,j,1) = CFDfiles(4,line_number)  ! TAWSS
c                     CFDresults_field(i,j,2) = CFDfiles(5,line_number)  ! OSI
c                     CFDresults_field(i,j,3) = CFDfiles(6,line_number)  ! ECAP
c                   else
c                     CFDresults_field(i,j,1) = 100  ! TAWSS
c                     CFDresults_field(i,j,2) = 100  ! OSI
c                     CFDresults_field(i,j,3) = 100  ! ECAP
c                   endif
c
c                 enddo
c               enddo
c
c             ! Option #3 - circumferential averaging of the results
c             elseif (luminal_surface_flag.eq.12.or.
c          &          luminal_surface_flag.eq.13) then
c               num_lines = line_number
c               do j = 2,nnz-1
c                 do k1 = 1,nnr
c                   if (nodemap(1,1,j-1,k1).eq.0) then
c                     exit
c                   endif
c                 enddo
c                 do k2 = 1,nnr
c                   if (nodemap(1,1,j,k2).eq.0) then
c                     exit
c                   endif
c                 enddo
c                 do k3 = 1,nnr
c                   if (nodemap(1,1,j+1,k3).eq.0) then
c                     exit
c                   endif
c                 enddo
c                 k1 = k1-1
c                 k2 = k2-1
c                 k3 = k3-1
c                 nd1 = nodemap(1,1,j-1,k1)
c                 nd2 = nodemap(1,1,j,k2)
c                 nd3 = nodemap(1,1,j+1,k3)
c
c                 ! Node z coordinates
c                 zz1 = x(3,nd1) + u(3,nd1)
c                 zz2 = x(3,nd2) + u(3,nd2)
c                 zz3 = x(3,nd3) + u(3,nd3)
c
c                 ! Layer boundaries for circumferential averaging
c                 zz_down = 0.5 * (zz1+zz2)
c                 zz_up   = 0.5 * (zz2+zz3)
c                 zz_down = zz_down - 0.75
c                 zz_up   = zz_up   + 0.75
c
c                 ! Loop over "kordinate" file to find nodes in the layer and average them
c                 layer_sum_result(1:3) = zero
c                 point_counter = 0
c                 do l = 1,num_lines
c                   zl = CFDfiles(3,l) * 1000 + translate_distance
c                   if (zl.ge.zz_down.and.zl.le.zz_up) then
c                     layer_sum_result(1) = layer_sum_result(1) +CFDfiles(4,l)
c                     layer_sum_result(2) = layer_sum_result(2) +CFDfiles(5,l)
c                     layer_sum_result(3) = layer_sum_result(3) +CFDfiles(6,l)
c                     point_counter = point_counter + 1
c                   endif
c                 enddo
c                 if (point_counter.eq.0) then
c                   layer_averaged_result(1:3) = 100
c                 else
c                   do k=1,3
c                   layer_averaged_result(k)=layer_sum_result(k)/point_counter
c                   enddo
c                 endif
c
c                 ! Save result values for current node
c                 CFDresults_field(1:nnt,j,1) = layer_averaged_result(1)  ! TAWSS
c                 CFDresults_field(1:nnt,j,2) = layer_averaged_result(2)  ! OSI
c                 CFDresults_field(1:nnt,j,3) = layer_averaged_result(3) ! ECAP
c
c               enddo
c
c               CFDresults_field(1:nnt,1,1)   = 100
c               CFDresults_field(1:nnt,1,2)   = 100
c               CFDresults_field(1:nnt,1,3)   = 100
c               CFDresults_field(1:nnt,nnz,1) = 100
c               CFDresults_field(1:nnt,nnz,2) = 100
c               CFDresults_field(1:nnt,nnz,3) = 100
c
c             endif ! Options
c
c           endif
c
c     c     Close and delete results files
c           close(50,status='delete')
c           close(51,status='delete')
c           close(52,status='delete')
c           close(53,status='delete')
c
c
c     c     Open file for writing feap CFD values
c           if (modfeap_number.eq.1) then
c             open(55,file='CFD_values_feap', status='replace',
c          &       action='write', form='formatted')
c             write(55,1005)
c             write(55,1013)
c           else
c             open(55,file='CFD_values_feap', status='old',
c          &       action='write', form='formatted')
c           endif
c
c           ! Write values to TAWSS_values_FEAP file
c           write(55,1006) modfeap_number
c           write(55,1009,advance='no')
c           do k = 1,nnt
c             write(55,1010,advance='no') k
c           enddo
c           write(55,1011,advance='no')
c           do k = 1,nnt
c             write(55,1012,advance='no')
c           enddo
c           write(55,*)
c           do i = 1,nnz
c             write(55,1008,advance='no') i
c             do k = 1,nnt
c               write(55,1007,advance='no') CFDresults_field(k,i,1)
c             enddo
c             write(55,*)
c             write(55,1014,advance='no')
c             do k = 1,nnt
c               write(55,1007,advance='no') CFDresults_field(k,i,2)
c             enddo
c             write(55,*)
c             write(55,1014,advance='no')
c             do k = 1,nnt
c               write(55,1007,advance='no') CFDresults_field(k,i,3)
c             enddo
c             write(55,*)
c             write(55,1014,advance='yes')
c           enddo
c           write(55,*)
c           close(55)
c
c           write(*,1004)
c
c     c-----------------------------------------------------------------------
c     1000  format(' "ECAP" file does not exist! Waiting for file ...')
c     1001  format(' "OSI" file does not exist! Waiting for file ...')
c     1002  format(' "TAWSS" file does not exist! Waiting for file ...')
c     1003  format(' "kordinate" file does not exist! Waiting for file ...')
c     1004  format(' CFD results files read. ')
c     1005  format(//1x 'CFD in lumen noded - interpolated from CFD
c          & results')
c     1006  format(/1x 'CFD analysis number', i3 /)
c     1007  format(f8.3)
c     1008  format(i7,' |')
c     1009  format(9x)
c     1010  format(i8)
c     1011  format(/8x '-')
c     1012  format('--------')
c     1013  format(/3x 'o--->            TAWSS' /
c          &        3x '|  theta           OSI' /
c          &        3x 'v z               ECAP' /)
c     1014  format(7x,' |')
c     1015  format(1x,'"CFDerrorA" file generated!')