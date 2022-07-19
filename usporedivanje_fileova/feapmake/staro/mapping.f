      subroutine mapping(x,u,lumsurface,ix,nodemap,elemmap,
     &           pressmap,angladd,iltlumnodes,rupture,ilt_elem_field,
     &           wallkc_field,rlnod)

c      Purpose: Runs at the beginning of simulation. Maps the inner
c               surface of cylinder (aorta). Based of external file
c               from fluid simulation outputs map location where to 
c               add elements.

c      Inputs:
c         x(ndm,numnp) - Nodal coordinates
c         ix(nen1,numel) - Element connection data

c      Outputs:


      implicit   none

      include   'user_ilt_flags.h'
      include   'cdata.h'
      include   'sdata.h'
      include   'comfil.h'
      include   'tdata.h'
      include   'mesh_parameters.h'
      include   'ilt_num_method_parameters.h'
      include   'user_model_options.h'
      include   'comblk.h'
      include   'pointer.h'
      !include   'mapp.h'
      
      real*8    x(ndm,numnp), u(ndf,numnp), lumsurface(nnt,nnz,2),
     &          rlnod(6,rlnod_size)
      integer   ix(nen1,numel), nodemap(9,nnt,nnz,nnr), 
     &          elemmap(nnt-1,nnz-1,nnr), pressmap(nnt-1,nnz-1),
     &          angladd(nnr,nnz),iltlumnodes(nnt,nnz), 
     &          rupture(ruptr_size), ilt_elem_field(8,iltel_size),
     &          wallkc_field(3,wall_numel) 
     
      real(kind=8), parameter :: zero=0d0, one=1d0, two=2d0, tol=1d-3
      logical   mapadd(nnt-1,nnz-1)
      
      
      integer   i,j,k,l,ii,jj,s,aa,n,layel,numlay,ndgen,eight, 
     &          nd,nd1,nd2,nd3,nd4,nd5,nd6,nd7,nd8,id1,id2,id3,
     &          npoint,nd_left,nd_right,nd_down,nd_up,nd_base,
     &          n1,n2,n3,n4,press_elem_number,mp1,mp2,mp3,mp4,side,
     &          updown,nd0,ndA,ndB,ndC,ndE,el,imn
      logical   newlayer,addlink,coor_title,link_title,elem_title,
     &          angl_title,boun_title,newlayer1,newlayer2,newlayer3,
     &          newlayer4,addnode1,addnode2,addnode3,addnode4,
     &          press_elem_title,ang,error1,add_in_nodepad,link_z,
     &          link_di_title
      real*8    angle(nnt)
      real*8    min_r,er,R,z,xx,yy,zmin,zmax,thmin,thmax,z1,z2,
     &          xx1,xx2,xx3,xx4,yy1,yy2,yy3,yy4,zz1,zz2,zz3,zz4,theta,
     &          theta1,theta2,pi,xx11,xx22,xx33,xx44,yy11,yy22,yy33,
     &          yy44,zz11,zz22,zz33,zz44,R1,R2,R3,R4,rD,zD,
     &          deg_to_rad,rad_to_deg,tmat,lum,rin,ru,zz,tau_int
      character lnk*30
      
      save      
c======================================================================      
      
c     Parameters      
      deg_to_rad = datan(1d0)/45d0
      rad_to_deg = 1/deg_to_rad
      
             
c     Open existing mesh files for new nodes and elements
      if(.not.open_new_mesh_files) then
             
        open(40,file='mesh-coor',status='old',
     &      action='write',form='formatted',position="append")
!        open(41,file='mesh-elem',status='old',
!     &      action='write',form='formatted',position="append")
      open(41,file='mesh-elem',status='replace',
     &      action='write',form='formatted',position="append")
        open(42,file='mesh-angl',status='replace',
     &      action='write',form='formatted',position="append")
        open(43,file='mesh-boun',status='replace',
     &      action='write',form='formatted',position="append")
        open(44,file='mesh-link',status='replace',
     &      action='write',form='formatted',position="append")
     
        if (move_pressure_flag) then
        open(45,file='mesh-elem-pr',status='replace',
     &      action='write',form='formatted',position="append")
        endif
        
        if (ilt_biochemo_flag.eq.3) then
          if (operating_system_flag.eq.1) then
            ! WINDOWS
            open(46,file='diffusion_elas\mesh-link-di',status='replace',
     &         action='write',form='formatted',position="append")
            open(47,file='diffusion_MMP\mesh-link-di',status='replace',
     &         action='write',form='formatted',position="append")
          else
            ! LINUX
            open(46,file='diffusion_elas/mesh-link-di',status='replace',
     &         action='write',form='formatted',position="append")
            open(47,file='diffusion_MMP/mesh-link-di',status='replace',
     &         action='write',form='formatted',position="append")
          endif
        endif
        
c       Turn off flags for writing titles in files
        coor_title  = .false.
        elem_title  = .false.
        angl_title  = .false.
        boun_title  = .false.
        link_title  = .false.
        press_elem_title = .false.
        link_di_title = .false.
      
      endif

c-----------------------------------------------------------------------
    
c     Open new mesh files for new nodes and elements
      if(open_new_mesh_files.and.initialize_map_flag) then
           
        node_number = numnp+1
        element_number = numel+1
        ilt_element_start_number = element_number
            
c       Create mesh files for new nodes and elements
             
        open(40,file='mesh-coor',status='replace',
     &      action='write',form='formatted',position="append")
        open(41,file='mesh-elem',status='replace',
     &      action='write',form='formatted',position="append")
        open(42,file='mesh-angl',status='replace',
     &      action='write',form='formatted',position="append")
        open(43,file='mesh-boun',status='replace',
     &      action='write',form='formatted',position="append")
        open(44,file='mesh-link',status='replace',
     &      action='write',form='formatted',position="append")
        open(45,file='mesh-elem-pr',status='replace',
     &      action='write',form='formatted',position="append")
     
        if (ilt_biochemo_flag.eq.3) then
          if (operating_system_flag.eq.1) then
            ! WINDOWS
            open(46,file='diffusion_elas\mesh-link-di',status='replace',
     &         action='write',form='formatted',position="append")
            open(47,file='diffusion_MMP\mesh-link-di',status='replace',
     &         action='write',form='formatted',position="append")
          else
            ! LINUX
            open(46,file='diffusion_elas/mesh-link-di',status='replace',
     &         action='write',form='formatted',position="append")
            open(47,file='diffusion_MMP/mesh-link-di',status='replace',
     &         action='write',form='formatted',position="append")
          endif
        endif
     
        open_new_mesh_files = .false.
      endif
      
c-----------------------------------------------------------------------
      
c     Read files with CFD results
      if (readCFD_flag) then
        call read_CFD_results(lumsurface,nodemap,x,u,hr(up(33)))
        readCFD_flag = .false.
      endif
      
c     Update luminal surface
      call update_lumsurface(lumsurface,nodemap,x,u,hr(up(33)))
      
c     Define mapadd field ie. area for possible ilt adding
      call define_mapadd(x,u,nodemap,mapadd,lumsurface)
      
c-----------------------------------------------------------------------
      
c     Write mesh-coor file (40)
      
      ndgen = 0
      
      do k = 1,nnr      ! razina
        do j = 1,nnz-1      ! z smjer
          do i = 1,nnt-1      ! theta smjer
              
            if(mapadd(i,j)) then  ! ako se na tu lokaciju dodaje element
              if(elemmap(i,j,k).eq.0) then  ! je li polje na toj razini prazno (nema elementa)
                
                ! Odredivanje radijusa povrsinskih cvorova na postojecem sloju ispod elementa i,j 
                ! n o d e  1 
                n1 = 0
                if(nodemap(1,i,j,k).ne.0) then  ! na mjestu cvora 1 se nalazi cvor postojeceg elementa
                  nd1 = nodemap(1,i,j,k)
                  xx1 = x(1,nd1) + u(1,nd1)
                  yy1 = x(2,nd1) + u(2,nd1)
                  R1 = sqrt(xx1**two + yy1**two)
                  newlayer1 = .false.
                else      ! cvor 1 nalazi se na novom sloju tj. nema postojecih cvorova na toj lokaciji
                  do while(nodemap(1,i,j,k-n1).eq.0)
                    n1 = n1+1
                  enddo
                  nd1 = nodemap(1,i,j,k-n1)
                  xx1 = x(1,nd1) + u(1,nd1)
                  yy1 = x(2,nd1) + u(2,nd1)
                  R1 = sqrt(xx1**two + yy1**two)
                  newlayer1 = .true.
                endif
                
                ! n o d e  2 
                n2 = 0
                if(nodemap(1,i,j+1,k).ne.0) then  ! na mjestu cvora 2 se nalazi cvor postojeceg elementa
                  nd2 = nodemap(1,i,j+1,k)
                  xx2 = x(1,nd2) + u(1,nd2)
                  yy2 = x(2,nd2) + u(2,nd2)
                  R2 = sqrt(xx2**two + yy2**two)
                  newlayer2 = .false.
                else      ! cvor 2 nalazi se na novom sloju tj. nema postojecih cvorova na toj lokaciji
                  do while(nodemap(1,i,j+1,k-n2).eq.0)
                    n2 = n2+1
                  enddo
                  nd2 = nodemap(1,i,j+1,k-n2)
                  xx2 = x(1,nd2) + u(1,nd2)
                  yy2 = x(2,nd2) + u(2,nd2)
                  R2 = sqrt(xx2**two + yy2**two)
                  newlayer2 = .true.
                endif
                
                ! n o d e  3 
                n3 = 0
                if(nodemap(1,i+1,j+1,k).ne.0) then  ! na mjestu cvora 3 se nalazi cvor postojeceg elementa
                  nd3 = nodemap(1,i+1,j+1,k)
                  xx3 = x(1,nd3) + u(1,nd3)
                  yy3 = x(2,nd3) + u(2,nd3)
                  R3 = sqrt(xx3**two + yy3**two)
                  newlayer3 = .false.
                else      ! cvor 3 nalazi se na novom sloju tj. nema postojecih cvorova na toj lokaciji
                  do while(nodemap(1,i+1,j+1,k-n3).eq.0)
                    n3 = n3+1
                  enddo
                  nd3 = nodemap(1,i+1,j+1,k-n3)
                  xx3 = x(1,nd3) + u(1,nd3)
                  yy3 = x(2,nd3) + u(2,nd3)
                  R3 = sqrt(xx3**two + yy3**two)
                  newlayer3 = .true.
                endif
                
                ! n o d e  4 
                n4 = 0
                if(nodemap(1,i+1,j,k).ne.0) then  ! na mjestu cvora 4 se nalazi cvor postojeceg elementa
                  nd4 = nodemap(1,i+1,j,k)
                  xx4 = x(1,nd4) + u(1,nd4)
                  yy4 = x(2,nd4) + u(2,nd4)
                  R4 = sqrt(xx4**two + yy4**two)
                  newlayer4 = .false.
                else      ! cvor 4 nalazi se na novom sloju tj. nema postojecih cvorova na toj lokaciji
                  do while(nodemap(1,i+1,j,k-n4).eq.0)
                    n4 = n4+1
                  enddo
                  nd4 = nodemap(1,i+1,j,k-n4)
                  xx4 = x(1,nd4) + u(1,nd4)
                  yy4 = x(2,nd4) + u(2,nd4)
                  R4 = sqrt(xx4**two + yy4**two)
                  newlayer4 = .true.
                endif
           
                ! Provjerava bi li dodani cvorovi bio ispod lumsurface
                if (k.gt.1) then
                  nd = elemmap(i,j,k-1)
                else
                  nd = 1
                endif
                
                addnode1 = .false.
                if (n1.eq.0.and.k.eq.1) then                  ! nalazim se na stijenci zile
                  if((R1-ilt_elem_th).ge.lumsurface(i,j,1)) then
                    addnode1 = .true.
                  endif
                elseif (n1.eq.0.and.k.gt.1.and.nd.ne.0) then  ! cvor 1 je na elementu tromba, a na lokaciji (i,j) ispod cvora 1 ima elementa
                  if((R1-ilt_elem_th).ge.lumsurface(i,j,1)) then
                    addnode1 = .true.
                  endif                  
                elseif (n1.eq.0.and.k.gt.1.and.nd.eq.0) then  ! cvor 1 je na elementu tromba, a na lokaciji (i,j) ispod cvora 1 nema elementa
                  if (nodemap(9,i,j,k-1).ne.0) then           ! morao sam prije dodati cvor ispod
                    addnode1 = .true.
                  endif
                else                                          ! cvor 1 se nalazi u prostoru iznad tromba i stijenke
                  if((R1-n1*ilt_elem_th).ge.lumsurface(i,j,1)) then 
                    addnode1 = .true.
                  endif  
                endif
                
                addnode2 = .false.
                if (n2.eq.0.and.k.eq.1) then                  ! nalazim se na stijenci zile
                  if((R2-ilt_elem_th).ge.lumsurface(i,j+1,1)) then
                    addnode2 = .true.
                  endif
                elseif (n2.eq.0.and.k.gt.1.and.nd.ne.0) then  ! cvor 2 je na elementu tromba, a na lokaciji (i,j) ispod cvora 2 ima elementa
                  if((R2-ilt_elem_th).ge.lumsurface(i,j+1,1)) then
                    addnode2 = .true.
                  endif                  
                elseif (n2.eq.0.and.k.gt.1.and.nd.eq.0) then  ! cvor 2 je na elementu tromba, a na lokaciji (i,j) ispod cvora 2 nema elementa
                  if (nodemap(9,i,j+1,k-1).ne.0) then         ! morao sam prije dodati cvor ispod
                    addnode2 = .true.
                  endif
                else                                          ! cvor 2 se nalazi u prostoru iznad tromba i stijenke
                  if((R2-n2*ilt_elem_th).ge.lumsurface(i,j+1,1)) then 
                    addnode2 = .true.
                  endif  
                endif
                
                addnode3 = .false.
                if (n3.eq.0.and.k.eq.1) then                  ! nalazim se na stijenci zile
                  if((R3-ilt_elem_th).ge.lumsurface(i+1,j+1,1)) then
                    addnode3 = .true.
                  endif
                elseif (n3.eq.0.and.k.gt.1.and.nd.ne.0) then  ! cvor 3 je na elementu tromba, a na lokaciji (i,j) ispod cvora 3 ima elementa
                  if((R3-ilt_elem_th).ge.lumsurface(i+1,j+1,1)) then
                    addnode3 = .true.
                  endif                  
                elseif (n3.eq.0.and.k.gt.1.and.nd.eq.0) then  ! cvor 3 je na elementu tromba, a na lokaciji (i,j) ispod cvora 3 nema elementa
                  if (nodemap(9,i+1,j+1,k-1).ne.0) then         ! morao sam prije dodati cvor ispod
                    addnode3 = .true.
                  endif
                else                                          ! cvor 3 se nalazi u prostoru iznad tromba i stijenke
                  if((R3-n3*ilt_elem_th).ge.lumsurface(i+1,j+1,1)) then 
                    addnode3 = .true.
                  endif  
                endif
                
                addnode4 = .false.
                if (n4.eq.0.and.k.eq.1) then                  ! nalazim se na stijenci zile
                  if((R4-ilt_elem_th).ge.lumsurface(i+1,j,1)) then
                    addnode4 = .true.
                  endif
                elseif (n4.eq.0.and.k.gt.1.and.nd.ne.0) then  ! cvor 4 je na elementu tromba, a na lokaciji (i,j) ispod cvora 4 ima elementa
                  if((R4-ilt_elem_th).ge.lumsurface(i+1,j,1)) then
                    addnode4 = .true.
                  endif                  
                elseif (n4.eq.0.and.k.gt.1.and.nd.eq.0) then  ! cvor 4 je na elementu tromba, a na lokaciji (i,j) ispod cvora 4 nema elementa
                  if (nodemap(9,i+1,j,k-1).ne.0) then         ! morao sam prije dodati cvor ispod
                    addnode4 = .true.
                  endif
                else                                          ! cvor 4 se nalazi u prostoru iznad tromba i stijenke
                  if((R4-n4*ilt_elem_th).ge.lumsurface(i+1,j,1)) then 
                    addnode4 = .true.
                  endif  
                endif
            
                ! Dodavanje cvorova i ispis u mesh-coor file    
                if(addnode1.and.addnode2.and.addnode3.and.addnode4) then
                
                  ! Dodaje cvor 1
                  if(newlayer1) then  ! na lokaciji (i,j,k) nema postojeceg cvora
                    ! xx1, yy1, R1 imam gore izracunato
                    if(nodemap(9,i,j,k).eq.0) then 
                      if(ilt_elem_growth_flag.eq.2.and.j.ne.1) then
                        ! ilt element se dodaje okomito na postojecu povrsinu
                        ndA = nodemap(1,i,j,k-n1)
                        ndB = nodemap(1,i,j+1,1)
                        ndC = nodemap(1,i,j-1,1)
                        call nodeD_position(x,u,ndA,ndB,ndC,n1,rD,zD)
                        xx11 = xx1*rD/R1
                        yy11 = yy1*rD/R1
                        zz11 = zD                      
                      else
                        nd1 = nodemap(1,i,j,k-n1)
                        xx11 = xx1*(R1-n1*ilt_elem_th)/R1
                        yy11 = yy1*(R1-n1*ilt_elem_th)/R1
                        zz11 = x(3,nd1)+u(3,nd1)
                      endif                 
                      if (.not.coor_title) then
                        write(40,*) 'COORdinates'
                        coor_title = .true.
                      endif                      
                      nodemap(9,i,j,k) = node_number 
                      write(40,1002) node_number,ndgen,xx11,yy11,zz11
                      node_number = node_number+1
                    endif
                  else  ! layer on old elements
                    if(nodemap(9,i,j,k).eq.0) then
                      if (.not.coor_title) then
                        write(40,*) 'COORdinates'
                        coor_title = .true.
                      endif 
                      nodemap(9,i,j,k) = node_number
                      nd1 = nodemap(1,i,j,k)
                      zz1 = x(3,nd1)+u(3,nd1)
                      write(40,1002) node_number,ndgen,xx1,yy1,zz1
                      node_number = node_number+1
                    endif
                  endif ! newlayer
                  
                  ! Dodaje cvor 2
                  if(newlayer2) then  ! na lokaciji (i,j,k) nema postojeceg cvora
                    ! xx2, yy2, R2 imam gore izracunato
                    if(nodemap(9,i,j+1,k).eq.0) then 
                      if(ilt_elem_growth_flag.eq.2.and.j.ne.(nnz-1))then
                        ! ilt element se dodaje okomito na postojecu povrsinu
                        ndA = nodemap(1,i,j+1,k-n2)
                        ndB = nodemap(1,i,j+2,1)
                        ndC = nodemap(1,i,j,1)
                        call nodeD_position(x,u,ndA,ndB,ndC,n2,rD,zD)
                        xx22 = xx2*rD/R2
                        yy22 = yy2*rD/R2
                        zz22 = zD
                      else
                        xx22 = xx2*(R2-n2*ilt_elem_th)/R2
                        yy22 = yy2*(R2-n2*ilt_elem_th)/R2
                        nd2 = nodemap(1,i,j+1,k-n2)
                        zz22 = x(3,nd2)+u(3,nd2)
                      endif                 
                      if (.not.coor_title) then
                        write(40,*) 'COORdinates'
                        coor_title = .true.
                      endif                      
                      nodemap(9,i,j+1,k) = node_number 
                      write(40,1002) node_number,ndgen,xx22,yy22,zz22
                      node_number = node_number+1
                    endif
                  else  ! layer on old elements
                    if(nodemap(9,i,j+1,k).eq.0) then
                      if (.not.coor_title) then
                        write(40,*) 'COORdinates'
                        coor_title = .true.
                      endif 
                      nodemap(9,i,j+1,k) = node_number
                      nd2 = nodemap(1,i,j+1,k)
                      zz2 = x(3,nd2)+u(3,nd2)
                      write(40,1002) node_number,ndgen,xx2,yy2,zz2
                      node_number = node_number+1
                    endif
                  endif ! newlayer
                  
                  ! Dodaje cvor 3
                  if(newlayer3) then  ! na lokaciji (i,j,k) nema postojeceg cvora
                    ! xx3, yy3, R3 imam gore izracunato
                    if(nodemap(9,i+1,j+1,k).eq.0) then 
                      if(ilt_elem_growth_flag.eq.2.and.j.ne.(nnz-1))then
                        ! ilt element se dodaje okomito na postojecu povrsinu
                        ndA = nodemap(1,i+1,j+1,k-n3)
                        ndB = nodemap(1,i+1,j+2,1)
                        ndC = nodemap(1,i+1,j,1)
                       call nodeD_position(x,u,ndA,ndB,ndC,n3,rD,zD)
                        xx33 = xx3*rD/R3
                        yy33 = yy3*rD/R3
                        zz33 = zD
                      else
                        xx33 = xx3*(R3-n3*ilt_elem_th)/R3
                        yy33 = yy3*(R3-n3*ilt_elem_th)/R3
                        nd3 = nodemap(1,i+1,j+1,k-n3)
                        zz33 = x(3,nd3)+u(3,nd3)
                      endif                 
                      if (.not.coor_title) then
                        write(40,*) 'COORdinates'
                        coor_title = .true.
                      endif                      
                      nodemap(9,i+1,j+1,k) = node_number 
                      write(40,1002) node_number,ndgen,xx33,yy33,zz33
                      node_number = node_number+1
                    endif
                  else  ! layer on old elements
                    if(nodemap(9,i+1,j+1,k).eq.0) then
                      if (.not.coor_title) then
                        write(40,*) 'COORdinates'
                        coor_title = .true.
                      endif 
                      nodemap(9,i+1,j+1,k) = node_number
                      nd3 = nodemap(1,i+1,j+1,k)
                      zz3 = x(3,nd3)+u(3,nd3)
                      write(40,1002) node_number,ndgen,xx3,yy3,zz3
                      node_number = node_number+1
                    endif
                  endif ! newlayer
                  
                  ! Dodaje cvor 4
                  if(newlayer4) then  ! na lokaciji (i,j,k) nema postojeceg cvora
                    ! xx4, yy4, R4 imam gore izracunato
                    if(nodemap(9,i+1,j,k).eq.0) then 
                      if(ilt_elem_growth_flag.eq.2.and.j.ne.1) then
                        ! ilt element se dodaje okomito na postojecu povrsinu
                        ndA = nodemap(1,i+1,j,k-n4)
                        ndB = nodemap(1,i+1,j+1,1)
                        ndC = nodemap(1,i+1,j-1,1)
                        call nodeD_position(x,u,ndA,ndB,ndC,n4,rD,zD)
                        xx44 = xx4*rD/R4
                        yy44 = yy4*rD/R4
                        zz44 = zD
                      else
                        xx44 = xx4*(R4-n4*ilt_elem_th)/R4
                        yy44 = yy4*(R4-n4*ilt_elem_th)/R4
                        nd4 = nodemap(1,i+1,j,k-n4)
                        zz44 = x(3,nd4)+u(3,nd4)
                      endif                 
                      if (.not.coor_title) then
                        write(40,*) 'COORdinates'
                        coor_title = .true.
                      endif                      
                      nodemap(9,i+1,j,k) = node_number 
                      write(40,1002) node_number,ndgen,xx44,yy44,zz44
                      node_number = node_number+1
                    endif
                  else  ! layer on old elements
                    if(nodemap(9,i+1,j,k).eq.0) then
                      if (.not.coor_title) then
                        write(40,*) 'COORdinates'
                        coor_title = .true.
                      endif 
                      nodemap(9,i+1,j,k) = node_number
                      nd4 = nodemap(1,i+1,j,k)
                      zz4 = x(3,nd4)+u(3,nd4)
                      write(40,1002) node_number,ndgen,xx4,yy4,zz4
                      node_number = node_number+1
                    endif
                  endif ! newlayer

                endif ! addnode1 ... addnode4
                  
              endif ! elemmap(i,j,k).ge.0
            endif ! mapadd(i,j).eq.true

          enddo   ! theta smjer
        enddo   ! z smjer
      enddo   ! razina
              
      if (coor_title) then
        write(40,*)
      endif

c-----------------------------------------------------------------------
      
c     Write mesh-elem file (41)
                
!      do k = 1,nnr-1    ! razina
!        do j = 1,nnz-1       ! z smjer
!          do i = 1,nnt-1       ! theta smjer
!            
!            nd1 = nodemap(9,   i,   j,   k)
!            nd2 = nodemap(9,   i, j+1,   k)
!            nd3 = nodemap(9, i+1, j+1,   k)
!            nd4 = nodemap(9, i+1,   j,   k)
!            nd5 = nodemap(9,   i,   j, k+1)
!            nd6 = nodemap(9,   i, j+1, k+1)
!            nd7 = nodemap(9, i+1, j+1, k+1)
!            nd8 = nodemap(9, i+1,   j, k+1)
!            !nd = nd1*nd2*nd3*nd4*nd5+nd6*nd7*nd8       ne valja
!            nd = 1
!            if (nd1.eq.0.or.nd2.eq.0.or.nd3.eq.0.or.nd4.eq.0.or.
!     &          nd5.eq.0.or.nd6.eq.0.or.nd7.eq.0.or.nd8.eq.0) then
!              nd = 0
!            endif
!            
!            if(elemmap(i,j,k).eq.0.and.nd.ne.0) then
!              
!              if (.not.elem_title) then
!                write(41,*) 'ELEMents'
!                elem_title = .true.
!              endif 
!              elemmap(i,j,k) = element_number
!              
!              write(41,1003) element_number,ndgen,ilt_mat_num,nd1,nd2,
!     &                       nd3,nd4,nd5,nd6,nd7,nd8
!              element_number = element_number+1
!              
!              add_in_nodepad = .true.
!              do l = 1,8
!                if (nd1.eq.nodemap(l,i,j,k)) then
!                  add_in_nodepad = .false.
!                endif
!              enddo
!              if (add_in_nodepad) then
!                if(nodemap(1,i,j,k).eq.0) then
!                  nodemap(1,i,j,k) = nd1
!                elseif(nodemap(2,i,j,k).eq.0) then
!                  nodemap(2,i,j,k) = nd1
!                elseif(nodemap(3,i,j,k).eq.0) then
!                  nodemap(3,i,j,k) = nd1
!                elseif(nodemap(4,i,j,k).eq.0) then
!                  nodemap(4,i,j,k) = nd1
!                elseif(nodemap(5,i,j,k).eq.0) then
!                  nodemap(5,i,j,k) = nd1
!                elseif(nodemap(6,i,j,k).eq.0) then
!                  nodemap(6,i,j,k) = nd1
!                elseif(nodemap(7,i,j,k).eq.0) then
!                  nodemap(7,i,j,k) = nd1
!                elseif(nodemap(8,i,j,k).eq.0) then
!                  nodemap(8,i,j,k) = nd1
!                endif
!              endif
!              
!              add_in_nodepad = .true.
!              do l = 1,8
!                if (nd2.eq.nodemap(l,i,j+1,k)) then
!                  add_in_nodepad = .false.
!                endif
!              enddo
!              if (add_in_nodepad) then
!                if(nodemap(1,i,j+1,k).eq.0) then
!                  nodemap(1,i,j+1,k) = nd2
!                elseif(nodemap(2,i,j+1,k).eq.0) then
!                  nodemap(2,i,j+1,k) = nd2
!                elseif(nodemap(3,i,j+1,k).eq.0) then
!                  nodemap(3,i,j+1,k) = nd2
!                elseif(nodemap(4,i,j+1,k).eq.0) then
!                  nodemap(4,i,j+1,k) = nd2
!                elseif(nodemap(5,i,j+1,k).eq.0) then
!                  nodemap(5,i,j+1,k) = nd2
!                elseif(nodemap(6,i,j+1,k).eq.0) then
!                  nodemap(6,i,j+1,k) = nd2
!                elseif(nodemap(7,i,j+1,k).eq.0) then
!                  nodemap(7,i,j+1,k) = nd2
!                elseif(nodemap(8,i,j+1,k).eq.0) then
!                  nodemap(8,i,j+1,k) = nd2
!                endif
!              endif
!              
!              add_in_nodepad = .true.
!              do l = 1,8
!                if (nd3.eq.nodemap(l,i+1,j+1,k)) then
!                  add_in_nodepad = .false.
!                endif
!              enddo
!              if (add_in_nodepad) then
!                if(nodemap(1,i+1,j+1,k).eq.0) then
!                  nodemap(1,i+1,j+1,k) = nd3
!                elseif(nodemap(2,i+1,j+1,k).eq.0) then
!                  nodemap(2,i+1,j+1,k) = nd3
!                elseif(nodemap(3,i+1,j+1,k).eq.0) then
!                  nodemap(3,i+1,j+1,k) = nd3
!                elseif(nodemap(4,i+1,j+1,k).eq.0) then
!                  nodemap(4,i+1,j+1,k) = nd3
!                elseif(nodemap(5,i+1,j+1,k).eq.0) then
!                  nodemap(5,i+1,j+1,k) = nd3
!                elseif(nodemap(6,i+1,j+1,k).eq.0) then
!                  nodemap(6,i+1,j+1,k) = nd3
!                elseif(nodemap(7,i+1,j+1,k).eq.0) then
!                  nodemap(7,i+1,j+1,k) = nd3
!                elseif(nodemap(8,i+1,j+1,k).eq.0) then
!                  nodemap(8,i+1,j+1,k) = nd3
!                endif
!              endif
!              
!              add_in_nodepad = .true.
!              do l = 1,8
!                if (nd4.eq.nodemap(l,i+1,j,k)) then
!                  add_in_nodepad = .false.
!                endif
!              enddo
!              if (add_in_nodepad) then
!                if(nodemap(1,i+1,j,k).eq.0) then
!                  nodemap(1,i+1,j,k) = nd4
!                elseif(nodemap(2,i+1,j,k).eq.0) then
!                  nodemap(2,i+1,j,k) = nd4
!                elseif(nodemap(3,i+1,j,k).eq.0) then
!                  nodemap(3,i+1,j,k) = nd4
!                elseif(nodemap(4,i+1,j,k).eq.0) then
!                  nodemap(4,i+1,j,k) = nd4
!                elseif(nodemap(5,i+1,j,k).eq.0) then
!                  nodemap(5,i+1,j,k) = nd4
!                elseif(nodemap(6,i+1,j,k).eq.0) then
!                  nodemap(6,i+1,j,k) = nd4
!                elseif(nodemap(7,i+1,j,k).eq.0) then
!                  nodemap(7,i+1,j,k) = nd4
!                elseif(nodemap(8,i+1,j,k).eq.0) then
!                  nodemap(8,i+1,j,k) = nd4
!                endif
!              endif
!              
!              add_in_nodepad = .true.
!              do l = 1,8
!                if (nd5.eq.nodemap(l,i,j,k+1)) then
!                  add_in_nodepad = .false.
!                endif
!              enddo
!              if (add_in_nodepad) then
!                if(nodemap(1,i,j,k+1).eq.0) then
!                  nodemap(1,i,j,k+1) = nd5
!                elseif(nodemap(2,i,j,k+1).eq.0) then
!                  nodemap(2,i,j,k+1) = nd5
!                elseif(nodemap(3,i,j,k+1).eq.0) then
!                  nodemap(3,i,j,k+1) = nd5
!                elseif(nodemap(4,i,j,k+1).eq.0) then
!                  nodemap(4,i,j,k+1) = nd5
!                elseif(nodemap(5,i,j,k+1).eq.0) then
!                  nodemap(5,i,j,k+1) = nd5
!                elseif(nodemap(6,i,j,k+1).eq.0) then
!                  nodemap(6,i,j,k+1) = nd5
!                elseif(nodemap(7,i,j,k+1).eq.0) then
!                  nodemap(7,i,j,k+1) = nd5
!                elseif(nodemap(8,i,j,k+1).eq.0) then
!                  nodemap(8,i,j,k+1) = nd5
!                endif
!              endif
!              
!              add_in_nodepad = .true.
!              do l = 1,8
!                if (nd6.eq.nodemap(l,i,j+1,k+1)) then
!                  add_in_nodepad = .false.
!                endif
!              enddo
!              if (add_in_nodepad) then
!                if(nodemap(1,i,j+1,k+1).eq.0) then
!                  nodemap(1,i,j+1,k+1) = nd6
!                elseif(nodemap(2,i,j+1,k+1).eq.0) then
!                  nodemap(2,i,j+1,k+1) = nd6
!                elseif(nodemap(3,i,j+1,k+1).eq.0) then
!                  nodemap(3,i,j+1,k+1) = nd6
!                elseif(nodemap(4,i,j+1,k+1).eq.0) then
!                  nodemap(4,i,j+1,k+1) = nd6
!                elseif(nodemap(5,i,j+1,k+1).eq.0) then
!                  nodemap(5,i,j+1,k+1) = nd6
!                elseif(nodemap(6,i,j+1,k+1).eq.0) then
!                  nodemap(6,i,j+1,k+1) = nd6
!                elseif(nodemap(7,i,j+1,k+1).eq.0) then
!                  nodemap(7,i,j+1,k+1) = nd6
!                elseif(nodemap(8,i,j+1,k+1).eq.0) then
!                  nodemap(8,i,j+1,k+1) = nd6
!                endif
!              endif
!              
!              add_in_nodepad = .true.
!              do l = 1,8
!                if (nd7.eq.nodemap(l,i+1,j+1,k+1)) then
!                  add_in_nodepad = .false.
!                endif
!              enddo
!              if (add_in_nodepad) then
!                if(nodemap(1,i+1,j+1,k+1).eq.0) then
!                  nodemap(1,i+1,j+1,k+1) = nd7
!                elseif(nodemap(2,i+1,j+1,k+1).eq.0) then
!                  nodemap(2,i+1,j+1,k+1) = nd7
!                elseif(nodemap(3,i+1,j+1,k+1).eq.0) then
!                  nodemap(3,i+1,j+1,k+1) = nd7
!                elseif(nodemap(4,i+1,j+1,k+1).eq.0) then
!                  nodemap(4,i+1,j+1,k+1) = nd7
!                elseif(nodemap(5,i+1,j+1,k+1).eq.0) then
!                  nodemap(5,i+1,j+1,k+1) = nd7
!                elseif(nodemap(6,i+1,j+1,k+1).eq.0) then
!                  nodemap(6,i+1,j+1,k+1) = nd7
!                elseif(nodemap(7,i+1,j+1,k+1).eq.0) then
!                  nodemap(7,i+1,j+1,k+1) = nd7
!                elseif(nodemap(8,i+1,j+1,k+1).eq.0) then
!                  nodemap(8,i+1,j+1,k+1) = nd7
!                endif
!              endif
!              
!              add_in_nodepad = .true.
!              do l = 1,8
!                if (nd8.eq.nodemap(l,i+1,j,k+1)) then
!                  add_in_nodepad = .false.
!                endif
!              enddo
!              if (add_in_nodepad) then
!                if(nodemap(1,i+1,j,k+1).eq.0) then
!                  nodemap(1,i+1,j,k+1) = nd8
!                elseif(nodemap(2,i+1,j,k+1).eq.0) then
!                  nodemap(2,i+1,j,k+1) = nd8
!                elseif(nodemap(3,i+1,j,k+1).eq.0) then
!                  nodemap(3,i+1,j,k+1) = nd8
!                elseif(nodemap(4,i+1,j,k+1).eq.0) then
!                  nodemap(4,i+1,j,k+1) = nd8
!                elseif(nodemap(5,i+1,j,k+1).eq.0) then
!                  nodemap(5,i+1,j,k+1) = nd8
!                elseif(nodemap(6,i+1,j,k+1).eq.0) then
!                  nodemap(6,i+1,j,k+1) = nd8
!                elseif(nodemap(7,i+1,j,k+1).eq.0) then
!                  nodemap(7,i+1,j,k+1) = nd8
!                elseif(nodemap(8,i+1,j,k+1).eq.0) then
!                  nodemap(8,i+1,j,k+1) = nd8
!                endif
!              endif
!              
!            endif
!            
!          enddo     ! theta smjer
!        enddo     ! z smjer
!      enddo     ! razina
!      if (elem_title) then
!        write(41,*)
!      endif
   
c-----------------------------------------------------------------------
      
c     Form elements and save them in element field
                
      do k = 1,nnr-1    ! razina
        do j = 1,nnz-1       ! z smjer
          do i = 1,nnt-1       ! theta smjer
            
            nd1 = nodemap(9,   i,   j,   k)
            nd2 = nodemap(9,   i, j+1,   k)
            nd3 = nodemap(9, i+1, j+1,   k)
            nd4 = nodemap(9, i+1,   j,   k)
            nd5 = nodemap(9,   i,   j, k+1)
            nd6 = nodemap(9,   i, j+1, k+1)
            nd7 = nodemap(9, i+1, j+1, k+1)
            nd8 = nodemap(9, i+1,   j, k+1)
            !nd = nd1*nd2*nd3*nd4*nd5+nd6*nd7*nd8       ne valja
            nd = 1
            if (nd1.eq.0.or.nd2.eq.0.or.nd3.eq.0.or.nd4.eq.0.or.
     &          nd5.eq.0.or.nd6.eq.0.or.nd7.eq.0.or.nd8.eq.0) then
              nd = 0
            endif
            
            if(elemmap(i,j,k).eq.0.and.nd.ne.0) then
               
              elemmap(i,j,k) = element_number
              el = element_number - wall_numnl_with_pr
              element_number = element_number+1
              
              ilt_elem_field(1,el) = nd1
              ilt_elem_field(2,el) = nd2
              ilt_elem_field(3,el) = nd3
              ilt_elem_field(4,el) = nd4
              ilt_elem_field(5,el) = nd5
              ilt_elem_field(6,el) = nd6
              ilt_elem_field(7,el) = nd7
              ilt_elem_field(8,el) = nd8
    
              add_in_nodepad = .true.
              do l = 1,8
                if (nd1.eq.nodemap(l,i,j,k)) then
                  add_in_nodepad = .false.
                endif
              enddo
              if (add_in_nodepad) then
                if(nodemap(1,i,j,k).eq.0) then
                  nodemap(1,i,j,k) = nd1
                elseif(nodemap(2,i,j,k).eq.0) then
                  nodemap(2,i,j,k) = nd1
                elseif(nodemap(3,i,j,k).eq.0) then
                  nodemap(3,i,j,k) = nd1
                elseif(nodemap(4,i,j,k).eq.0) then
                  nodemap(4,i,j,k) = nd1
                elseif(nodemap(5,i,j,k).eq.0) then
                  nodemap(5,i,j,k) = nd1
                elseif(nodemap(6,i,j,k).eq.0) then
                  nodemap(6,i,j,k) = nd1
                elseif(nodemap(7,i,j,k).eq.0) then
                  nodemap(7,i,j,k) = nd1
                elseif(nodemap(8,i,j,k).eq.0) then
                  nodemap(8,i,j,k) = nd1
                endif
              endif
              
              add_in_nodepad = .true.
              do l = 1,8
                if (nd2.eq.nodemap(l,i,j+1,k)) then
                  add_in_nodepad = .false.
                endif
              enddo
              if (add_in_nodepad) then
                if(nodemap(1,i,j+1,k).eq.0) then
                  nodemap(1,i,j+1,k) = nd2
                elseif(nodemap(2,i,j+1,k).eq.0) then
                  nodemap(2,i,j+1,k) = nd2
                elseif(nodemap(3,i,j+1,k).eq.0) then
                  nodemap(3,i,j+1,k) = nd2
                elseif(nodemap(4,i,j+1,k).eq.0) then
                  nodemap(4,i,j+1,k) = nd2
                elseif(nodemap(5,i,j+1,k).eq.0) then
                  nodemap(5,i,j+1,k) = nd2
                elseif(nodemap(6,i,j+1,k).eq.0) then
                  nodemap(6,i,j+1,k) = nd2
                elseif(nodemap(7,i,j+1,k).eq.0) then
                  nodemap(7,i,j+1,k) = nd2
                elseif(nodemap(8,i,j+1,k).eq.0) then
                  nodemap(8,i,j+1,k) = nd2
                endif
              endif
              
              add_in_nodepad = .true.
              do l = 1,8
                if (nd3.eq.nodemap(l,i+1,j+1,k)) then
                  add_in_nodepad = .false.
                endif
              enddo
              if (add_in_nodepad) then
                if(nodemap(1,i+1,j+1,k).eq.0) then
                  nodemap(1,i+1,j+1,k) = nd3
                elseif(nodemap(2,i+1,j+1,k).eq.0) then
                  nodemap(2,i+1,j+1,k) = nd3
                elseif(nodemap(3,i+1,j+1,k).eq.0) then
                  nodemap(3,i+1,j+1,k) = nd3
                elseif(nodemap(4,i+1,j+1,k).eq.0) then
                  nodemap(4,i+1,j+1,k) = nd3
                elseif(nodemap(5,i+1,j+1,k).eq.0) then
                  nodemap(5,i+1,j+1,k) = nd3
                elseif(nodemap(6,i+1,j+1,k).eq.0) then
                  nodemap(6,i+1,j+1,k) = nd3
                elseif(nodemap(7,i+1,j+1,k).eq.0) then
                  nodemap(7,i+1,j+1,k) = nd3
                elseif(nodemap(8,i+1,j+1,k).eq.0) then
                  nodemap(8,i+1,j+1,k) = nd3
                endif
              endif
              
              add_in_nodepad = .true.
              do l = 1,8
                if (nd4.eq.nodemap(l,i+1,j,k)) then
                  add_in_nodepad = .false.
                endif
              enddo
              if (add_in_nodepad) then
                if(nodemap(1,i+1,j,k).eq.0) then
                  nodemap(1,i+1,j,k) = nd4
                elseif(nodemap(2,i+1,j,k).eq.0) then
                  nodemap(2,i+1,j,k) = nd4
                elseif(nodemap(3,i+1,j,k).eq.0) then
                  nodemap(3,i+1,j,k) = nd4
                elseif(nodemap(4,i+1,j,k).eq.0) then
                  nodemap(4,i+1,j,k) = nd4
                elseif(nodemap(5,i+1,j,k).eq.0) then
                  nodemap(5,i+1,j,k) = nd4
                elseif(nodemap(6,i+1,j,k).eq.0) then
                  nodemap(6,i+1,j,k) = nd4
                elseif(nodemap(7,i+1,j,k).eq.0) then
                  nodemap(7,i+1,j,k) = nd4
                elseif(nodemap(8,i+1,j,k).eq.0) then
                  nodemap(8,i+1,j,k) = nd4
                endif
              endif
              
              add_in_nodepad = .true.
              do l = 1,8
                if (nd5.eq.nodemap(l,i,j,k+1)) then
                  add_in_nodepad = .false.
                endif
              enddo
              if (add_in_nodepad) then
                if(nodemap(1,i,j,k+1).eq.0) then
                  nodemap(1,i,j,k+1) = nd5
                elseif(nodemap(2,i,j,k+1).eq.0) then
                  nodemap(2,i,j,k+1) = nd5
                elseif(nodemap(3,i,j,k+1).eq.0) then
                  nodemap(3,i,j,k+1) = nd5
                elseif(nodemap(4,i,j,k+1).eq.0) then
                  nodemap(4,i,j,k+1) = nd5
                elseif(nodemap(5,i,j,k+1).eq.0) then
                  nodemap(5,i,j,k+1) = nd5
                elseif(nodemap(6,i,j,k+1).eq.0) then
                  nodemap(6,i,j,k+1) = nd5
                elseif(nodemap(7,i,j,k+1).eq.0) then
                  nodemap(7,i,j,k+1) = nd5
                elseif(nodemap(8,i,j,k+1).eq.0) then
                  nodemap(8,i,j,k+1) = nd5
                endif
              endif
              
              add_in_nodepad = .true.
              do l = 1,8
                if (nd6.eq.nodemap(l,i,j+1,k+1)) then
                  add_in_nodepad = .false.
                endif
              enddo
              if (add_in_nodepad) then
                if(nodemap(1,i,j+1,k+1).eq.0) then
                  nodemap(1,i,j+1,k+1) = nd6
                elseif(nodemap(2,i,j+1,k+1).eq.0) then
                  nodemap(2,i,j+1,k+1) = nd6
                elseif(nodemap(3,i,j+1,k+1).eq.0) then
                  nodemap(3,i,j+1,k+1) = nd6
                elseif(nodemap(4,i,j+1,k+1).eq.0) then
                  nodemap(4,i,j+1,k+1) = nd6
                elseif(nodemap(5,i,j+1,k+1).eq.0) then
                  nodemap(5,i,j+1,k+1) = nd6
                elseif(nodemap(6,i,j+1,k+1).eq.0) then
                  nodemap(6,i,j+1,k+1) = nd6
                elseif(nodemap(7,i,j+1,k+1).eq.0) then
                  nodemap(7,i,j+1,k+1) = nd6
                elseif(nodemap(8,i,j+1,k+1).eq.0) then
                  nodemap(8,i,j+1,k+1) = nd6
                endif
              endif
              
              add_in_nodepad = .true.
              do l = 1,8
                if (nd7.eq.nodemap(l,i+1,j+1,k+1)) then
                  add_in_nodepad = .false.
                endif
              enddo
              if (add_in_nodepad) then
                if(nodemap(1,i+1,j+1,k+1).eq.0) then
                  nodemap(1,i+1,j+1,k+1) = nd7
                elseif(nodemap(2,i+1,j+1,k+1).eq.0) then
                  nodemap(2,i+1,j+1,k+1) = nd7
                elseif(nodemap(3,i+1,j+1,k+1).eq.0) then
                  nodemap(3,i+1,j+1,k+1) = nd7
                elseif(nodemap(4,i+1,j+1,k+1).eq.0) then
                  nodemap(4,i+1,j+1,k+1) = nd7
                elseif(nodemap(5,i+1,j+1,k+1).eq.0) then
                  nodemap(5,i+1,j+1,k+1) = nd7
                elseif(nodemap(6,i+1,j+1,k+1).eq.0) then
                  nodemap(6,i+1,j+1,k+1) = nd7
                elseif(nodemap(7,i+1,j+1,k+1).eq.0) then
                  nodemap(7,i+1,j+1,k+1) = nd7
                elseif(nodemap(8,i+1,j+1,k+1).eq.0) then
                  nodemap(8,i+1,j+1,k+1) = nd7
                endif
              endif
              
              add_in_nodepad = .true.
              do l = 1,8
                if (nd8.eq.nodemap(l,i+1,j,k+1)) then
                  add_in_nodepad = .false.
                endif
              enddo
              if (add_in_nodepad) then
                if(nodemap(1,i+1,j,k+1).eq.0) then
                  nodemap(1,i+1,j,k+1) = nd8
                elseif(nodemap(2,i+1,j,k+1).eq.0) then
                  nodemap(2,i+1,j,k+1) = nd8
                elseif(nodemap(3,i+1,j,k+1).eq.0) then
                  nodemap(3,i+1,j,k+1) = nd8
                elseif(nodemap(4,i+1,j,k+1).eq.0) then
                  nodemap(4,i+1,j,k+1) = nd8
                elseif(nodemap(5,i+1,j,k+1).eq.0) then
                  nodemap(5,i+1,j,k+1) = nd8
                elseif(nodemap(6,i+1,j,k+1).eq.0) then
                  nodemap(6,i+1,j,k+1) = nd8
                elseif(nodemap(7,i+1,j,k+1).eq.0) then
                  nodemap(7,i+1,j,k+1) = nd8
                elseif(nodemap(8,i+1,j,k+1).eq.0) then
                  nodemap(8,i+1,j,k+1) = nd8
                endif
              endif
              
            endif
            
          enddo     ! theta smjer
        enddo     ! z smjer
      enddo     ! razina

c     Write mesh_elem file (41)
      if (ilt_elem_field(1,1).ne.0) then
        write(41,*) 'ELEMents'
        
        do i = wall_numnl_with_pr+1, element_number-1
          el = i - wall_numnl_with_pr
          nd1 = ilt_elem_field(1,el)
          nd2 = ilt_elem_field(2,el)
          nd3 = ilt_elem_field(3,el)
          nd4 = ilt_elem_field(4,el)
          nd5 = ilt_elem_field(5,el)
          nd6 = ilt_elem_field(6,el)
          nd7 = ilt_elem_field(7,el)
          nd8 = ilt_elem_field(8,el)
          
          if (rupture(i).eq.1) then
            imn = ilt_mat_num_rupt
          else
            imn = ilt_mat_num
          endif
          
          write(41,1003) i,ndgen,imn,nd1,nd2,nd3,nd4,nd5,nd6,nd7,nd8
        enddo
        
        write(41,*)
        
      endif
      
c-----------------------------------------------------------------------
      
c     Write new pressure elements in file
      press_elem_number = element_number
      if(move_pressure_flag) then
        
        ! elementi tlaka na povrsini tromba
        do k = 2,nnr-1
          do j = 1,nnz-1
            do i = 1,nnt-1
              if(elemmap(i,j,k-1).ne.0.and.elemmap(i,j,k).eq.0) then
                nd1 = nodemap(1,i,j,k)
                nd2 = nodemap(1,i,j+1,k)
                nd3 = nodemap(1,i+1,j+1,k)
                nd4 = nodemap(1,i+1,j,k)
                if(.not.press_elem_title) then
                  write(45,*) 'ELEMents'
                  press_elem_title = .true.
                endif 
                write(45,1003) press_elem_number,ndgen,press_mat_num,
     &                         nd1,nd2,nd3,nd4,zero,zero,zero,zero
                press_elem_number = press_elem_number+1
              endif
            enddo
          enddo
        enddo
        
        ! elementi suprotnog tlaka na stijenci ispod tromba
        do j = 1,nnz-1
          do i = 1,nnt-1
            if (elemmap(i,j,1).ne.0) then
              nd1 = nodemap(1,i,j,1)
              nd2 = nodemap(1,i,j+1,1)
              nd3 = nodemap(1,i+1,j+1,1)
              nd4 = nodemap(1,i+1,j,1)
              if(.not.press_elem_title) then
                write(45,*) 'ELEMents'
                press_elem_title = .true.
              endif
              write(45,1003) press_elem_number,ndgen,zero_press_mat_num,
     &                        nd1,nd2,nd3,nd4,zero,zero,zero,zero
              press_elem_number = press_elem_number+1
            endif
          enddo
        enddo
        
      endif
      
c-----------------------------------------------------------------------
     
c     Write mesh-boun file (43) and mesh-angl file (42)
      
      ! Calculate boundary angle
      do i = 1,nnt
        nd = nodemap(1,i,1,1)
        xx = x(1,nd)
        yy = x(2,nd)
        R = dsqrt(xx**two + yy**two)
        if (yy.ge.(zero-tol)) then
          theta = dacos(xx/R)
        else
          theta = dacos(-one) + dacos(-xx/R)
        endif
        angle(i) = rad_to_deg*theta
      enddo
      
      if (ilt_boundary_flag.eq.1) then
      
        do k = 1,nnr      ! razina
          do i = 1,nnt      ! theta smjer
            do j = 1,nnz      ! z smjer
              
              ! --- mesh-boun file (43) ---
              if (.not.boun_title) then
                write(43,*) 'BOUNdary conditions'
                boun_title = .true.
              endif
              side = zero
              updown = zero
              if (j.eq.1.or.j.eq.nnz) then
                updown = one
              endif
              if (i.eq.1.or.i.eq.nnt) then
                side = one
              endif
              
              nd1 = nodemap(1,i,j,k)
              nd2 = nodemap(2,i,j,k)
              nd3 = nodemap(3,i,j,k)
              nd4 = nodemap(4,i,j,k)
              nd5 = nodemap(5,i,j,k)
              nd6 = nodemap(6,i,j,k)
              nd7 = nodemap(7,i,j,k)
              nd8 = nodemap(8,i,j,k)
              
              if ((side+updown).ne.0) then  ! ako se cvor nalazi na rubu
                if (k.gt.1.and.nd1.ne.0) then ! za k=1 cvor nd1 pripada stijenci i njemu su RU vec definirani
                  write(43,1005) nd1, ndgen, zero,side,updown
                endif
                if (nd2.ne.0) write(43,1005) nd2, ndgen,zero,side,updown
                if (nd3.ne.0) write(43,1005) nd3, ndgen,zero,side,updown
                if (nd4.ne.0) write(43,1005) nd4, ndgen,zero,side,updown
                if (nd5.ne.0) write(43,1005) nd5, ndgen,zero,side,updown
                if (nd6.ne.0) write(43,1005) nd6, ndgen,zero,side,updown
                if (nd7.ne.0) write(43,1005) nd7, ndgen,zero,side,updown
                if (nd8.ne.0) write(43,1005) nd8, ndgen,zero,side,updown
              endif
            
              ! --- mesh-angl file (42) ---
              if (.not.angl_title) then
                write(42,*) 'ANGLe conditions'
                angl_title = .true.
              endif
              
              ! cvorovi na stijenci
              if (i.ne.1.and.i.ne.nnt.and.k.eq.1) then  
                nd = nodemap(1,i,j,k)
                write(42,1004) nd, ndgen, angle(i)
              endif
              
              ! cvorovi na trombu
              if (k.gt.1.and.nd1.ne.0) then ! za k=1 cvor nd1 pripada stijenci i njemu su RU vec definirani
                write(42,1004) nd1, ndgen, angle(i)
              endif
              if (nd2.ne.0) write(42,1004) nd2, ndgen, angle(i)
              if (nd3.ne.0) write(42,1004) nd3, ndgen, angle(i)
              if (nd4.ne.0) write(42,1004) nd4, ndgen, angle(i)
              if (nd5.ne.0) write(42,1004) nd5, ndgen, angle(i)
              if (nd6.ne.0) write(42,1004) nd6, ndgen, angle(i)
              if (nd7.ne.0) write(42,1004) nd7, ndgen, angle(i)
              if (nd8.ne.0) write(42,1004) nd8, ndgen, angle(i)
          
              
              ! --- mesh-link file (44) ---
              id1 = zero
              id2 = side
              id3 = updown
              ! spajanje slojeva
              if (nd2.ne.0) then
                if (.not.link_title) then
                  write(44,*) 'LINK'
                  link_title = .true.
                endif
                write(44,1006) nd2,nd1, 0,0, id1,id2,id3
              endif
              if (nd3.ne.0) write(44,1006) nd3,nd1, 0,0, id1,id2,id3
              if (nd4.ne.0) write(44,1006) nd4,nd1, 0,0, id1,id2,id3
              if (nd5.ne.0) write(44,1006) nd5,nd1, 0,0, id1,id2,id3
              if (nd6.ne.0) write(44,1006) nd6,nd1, 0,0, id1,id2,id3
              if (nd7.ne.0) write(44,1006) nd7,nd1, 0,0, id1,id2,id3
              if (nd8.ne.0) write(44,1006) nd8,nd1, 0,0, id1,id2,id3

              ! spajanje slobodnih cvorova s bazom
              if (k.gt.1.and.nd1.ne.0) then
                if ((i.eq.1.or.i.eq.nnt).and.(j.eq.1.or.j.eq.nnz)) then! cvorovi u kutevima
                  ! cvorovi se ne spajaju jer su ograniceni rubnim uvjetima
                elseif (i.eq.1.or.i.eq.nnt) then  ! bocne linije (linkanje samo u z smjeru)
                  nd_up = nodemap(1,i,j+1,k)
                  nd_down = nodemap(1,i,j-1,k)
                  nd_base = nodemap(1,i,j,1)
                  if (nd_up.eq.0.or.nd_down.eq.0) then
                    write(44,1006) nd1,nd_base, 0,0, 1, 1, 0
                  endif
                elseif (j.eq.1.or.j.eq.nnz) then  ! gornja i donja linija (linkanje samo u theta smjeru)
                  nd_left = nodemap(1,i-1,j,k)
                  nd_right = nodemap(1,i+1,j,k)
                  nd_base = nodemap(1,i,j,1)
                  if (nd_left.eq.0.or.nd_right.eq.0) then
                    write(44,1006) nd1,nd_base, 0,0, 1, 0, 1
                  endif
                else
                  nd_up = nodemap(1,i,j+1,k)
                  nd_down = nodemap(1,i,j-1,k)
                  nd_left = nodemap(1,i-1,j,k)
                  nd_right = nodemap(1,i+1,j,k)
                  nd_base = nodemap(1,i,j,1)
                  if (nd_up.eq.0.or.nd_down.eq.0.or.nd_left.eq.0.or.
     &                nd_right.eq.0) then
                    id2 = 1
                    id3 = 1
                    if (nd_up.eq.0.or.nd_down.eq.0)     id3 = 0
                    if (nd_left.eq.0.or.nd_right.eq.0)  id2 = 0
                    write(44,1006) nd1,nd_base, 0,0, 1, id2, id3
                  endif
                endif
              endif
              
            enddo     ! j
          enddo     ! i
        enddo     ! k
        
     
      elseif (ilt_boundary_flag.eq.2) then
        
        do k = 1,nnr      ! razina
          do i = 1,nnt      ! theta smjer
            do j = 1,nnz      ! z smjer
              
              ! --- mesh-boun file (43) ---
              if (.not.boun_title) then
                write(43,*) 'BOUNdary conditions'
                boun_title = .true.
              endif
              side = zero
              updown = zero
              link_z = .false.
              
              nd1 = nodemap(1,i,j,k)
              nd2 = nodemap(2,i,j,k)
              nd3 = nodemap(3,i,j,k)
              nd4 = nodemap(4,i,j,k)
              nd5 = nodemap(5,i,j,k)
              nd6 = nodemap(6,i,j,k)
              nd7 = nodemap(7,i,j,k)
              nd8 = nodemap(8,i,j,k)
              
              if ((i.eq.1.or.i.eq.nnt).and.(j.eq.1.or.j.eq.nnz)) then! cvorovi u kutevima
                side = one
                updown = one
              elseif (i.eq.1.or.i.eq.nnt) then  ! bocne linije
                side = one
                nd_up = nodemap(1,i,j+1,k)
                nd_down = nodemap(1,i,j-1,k)
                if (nd_up.eq.0.or.nd_down.eq.0) updown = one
              elseif (j.eq.1.or.j.eq.nnz) then  ! gornja i donja linija
                updown = one
                nd_left = nodemap(1,i-1,j,k)
                nd_right = nodemap(1,i+1,j,k)
                if (nd_left.eq.0.or.nd_right.eq.0) side = one
              else
                nd_up = nodemap(1,i,j+1,k)
                nd_down = nodemap(1,i,j-1,k)
                nd_left = nodemap(1,i-1,j,k)
                nd_right = nodemap(1,i+1,j,k)
                nd_base = nodemap(1,i,j,1)
                if (k.gt.1.and.nd1.ne.0.and.
     &             (nd_up.eq.0.or.nd_down.eq.0)) link_z = .true.
                if (nd_left.eq.0.or.nd_right.eq.0)  side = one
              endif
              
              if ((side+updown).ne.0) then  ! ako se cvor nalazi na rubu
                if (k.gt.1.and.nd1.ne.0) then ! za k=1 cvor nd1 pripada stijenci i njemu su RU vec definirani
                  write(43,1005) nd1, ndgen, zero,side,updown
                endif
                if (nd2.ne.0) write(43,1005) nd2, ndgen,zero,side,updown
                if (nd3.ne.0) write(43,1005) nd3, ndgen,zero,side,updown
                if (nd4.ne.0) write(43,1005) nd4, ndgen,zero,side,updown
                if (nd5.ne.0) write(43,1005) nd5, ndgen,zero,side,updown
                if (nd6.ne.0) write(43,1005) nd6, ndgen,zero,side,updown
                if (nd7.ne.0) write(43,1005) nd7, ndgen,zero,side,updown
                if (nd8.ne.0) write(43,1005) nd8, ndgen,zero,side,updown
              endif
            
              ! --- mesh-angl file (42) ---
              if (.not.angl_title) then
                write(42,*) 'ANGLe conditions'
                angl_title = .true.
              endif
              
              ! cvorovi na stijenci
              if (i.ne.1.and.i.ne.nnt.and.k.eq.1) then  
                nd = nodemap(1,i,j,k)
                write(42,1004) nd, ndgen, angle(i)
              endif
              
              ! cvorovi na trombu
              if (k.gt.1.and.nd1.ne.0) then ! za k=1 cvor nd1 pripada stijenci i njemu su RU vec definirani
                write(42,1004) nd1, ndgen, angle(i)
              endif
              if (nd2.ne.0) write(42,1004) nd2, ndgen, angle(i)
              if (nd3.ne.0) write(42,1004) nd3, ndgen, angle(i)
              if (nd4.ne.0) write(42,1004) nd4, ndgen, angle(i)
              if (nd5.ne.0) write(42,1004) nd5, ndgen, angle(i)
              if (nd6.ne.0) write(42,1004) nd6, ndgen, angle(i)
              if (nd7.ne.0) write(42,1004) nd7, ndgen, angle(i)
              if (nd8.ne.0) write(42,1004) nd8, ndgen, angle(i)
          
              
              ! --- mesh-link file (44) ---
              id1 = zero
              id2 = side
              id3 = updown
              ! spajanje slojeva
              if (nd2.ne.0) then
                if (.not.link_title) then
                  write(44,*) 'LINK'
                  link_title = .true.
                endif
                write(44,1006) nd2,nd1, 0,0, id1,id2,id3
              endif
              if (nd3.ne.0) write(44,1006) nd3,nd1, 0,0, id1,id2,id3
              if (nd4.ne.0) write(44,1006) nd4,nd1, 0,0, id1,id2,id3
              if (nd5.ne.0) write(44,1006) nd5,nd1, 0,0, id1,id2,id3
              if (nd6.ne.0) write(44,1006) nd6,nd1, 0,0, id1,id2,id3
              if (nd7.ne.0) write(44,1006) nd7,nd1, 0,0, id1,id2,id3
              if (nd8.ne.0) write(44,1006) nd8,nd1, 0,0, id1,id2,id3
              
              ! spajanje sa baznim cvorom u z smjeru
              if (link_z) then
                write(44,1006) nd1,nd_base, 0,0, 1,1,0
              endif

            enddo     ! j
          enddo     ! i
        enddo     ! k
      
      else ! (ilt_boundary_flag.eq.3)
        
        do k = 1,nnr      ! razina
          do i = 1,nnt      ! theta smjer
            do j = 1,nnz      ! z smjer
              
              ! --- mesh-boun file (43) ---
              if (.not.boun_title) then
                write(43,*) 'BOUNdary conditions'
                boun_title = .true.
              endif
              side = zero
              updown = zero
              if (j.eq.1.or.j.eq.nnz) then
                updown = one
              endif
              if (i.eq.1.or.i.eq.nnt) then
                side = one
              endif
              
              nd1 = nodemap(1,i,j,k)
              nd2 = nodemap(2,i,j,k)
              nd3 = nodemap(3,i,j,k)
              nd4 = nodemap(4,i,j,k)
              nd5 = nodemap(5,i,j,k)
              nd6 = nodemap(6,i,j,k)
              nd7 = nodemap(7,i,j,k)
              nd8 = nodemap(8,i,j,k)
              
              if ((side+updown).ne.0) then  ! ako se cvor nalazi na rubu
                if (k.gt.1.and.nd1.ne.0) then ! za k=1 cvor nd1 pripada stijenci i njemu su RU vec definirani
                  write(43,1005) nd1, ndgen, zero,side,updown
                endif
                if (nd2.ne.0) write(43,1005) nd2, ndgen,zero,side,updown
                if (nd3.ne.0) write(43,1005) nd3, ndgen,zero,side,updown
                if (nd4.ne.0) write(43,1005) nd4, ndgen,zero,side,updown
                if (nd5.ne.0) write(43,1005) nd5, ndgen,zero,side,updown
                if (nd6.ne.0) write(43,1005) nd6, ndgen,zero,side,updown
                if (nd7.ne.0) write(43,1005) nd7, ndgen,zero,side,updown
                if (nd8.ne.0) write(43,1005) nd8, ndgen,zero,side,updown
              endif
            
              ! --- mesh-angl file (42) ---
              if (.not.angl_title) then
                write(42,*) 'ANGLe conditions'
                angl_title = .true.
              endif

              ! cvorovi tromba na rubu
              if (i.eq.1.or.i.eq.nnt) then
                if (k.gt.1.and.nd1.ne.0) then ! za k=1 cvor nd1 pripada stijenci i njemu su RU vec definirani
                  write(42,1004) nd1, ndgen, angle(i)
                endif
                if (nd2.ne.0) write(42,1004) nd2, ndgen, angle(i)
                if (nd3.ne.0) write(42,1004) nd3, ndgen, angle(i)
                if (nd4.ne.0) write(42,1004) nd4, ndgen, angle(i)
                if (nd5.ne.0) write(42,1004) nd5, ndgen, angle(i)
                if (nd6.ne.0) write(42,1004) nd6, ndgen, angle(i)
                if (nd7.ne.0) write(42,1004) nd7, ndgen, angle(i)
                if (nd8.ne.0) write(42,1004) nd8, ndgen, angle(i)
              endif
          
              
              ! --- mesh-link file (44) ---
              id1 = zero
              id2 = side
              id3 = updown
              ! spajanje slojeva
              if (nd2.ne.0) then
                if (.not.link_title) then
                  write(44,*) 'LINK'
                  link_title = .true.
                endif
                write(44,1006) nd2,nd1, 0,0, id1,id2,id3
              endif
              if (nd3.ne.0) write(44,1006) nd3,nd1, 0,0, id1,id2,id3
              if (nd4.ne.0) write(44,1006) nd4,nd1, 0,0, id1,id2,id3
              if (nd5.ne.0) write(44,1006) nd5,nd1, 0,0, id1,id2,id3
              if (nd6.ne.0) write(44,1006) nd6,nd1, 0,0, id1,id2,id3
              if (nd7.ne.0) write(44,1006) nd7,nd1, 0,0, id1,id2,id3
              if (nd8.ne.0) write(44,1006) nd8,nd1, 0,0, id1,id2,id3
              
            enddo     ! j
          enddo     ! i
        enddo     ! k 
        
      endif   ! ilt_boundary_flag.eq.3
      
      
      if (ilt_biochemo_flag.eq.3) then
      
        do k = 1,nnr      ! razina
          do i = 1,nnt      ! theta smjer
            do j = 1,nnz      ! z smjer
            
              nd1 = nodemap(1,i,j,k)
              nd2 = nodemap(2,i,j,k)
              nd3 = nodemap(3,i,j,k)
              nd4 = nodemap(4,i,j,k)
              nd5 = nodemap(5,i,j,k)
              nd6 = nodemap(6,i,j,k)
              nd7 = nodemap(7,i,j,k)
              nd8 = nodemap(8,i,j,k)
              
              ! --- mesh-link-di file (46) ---
              id1 = zero
              id2 = one
              id3 = one
              ! spajanje slojeva
              if (nd2.ne.0) then
                if (.not.link_di_title) then
                  write(46,*) 'LINK'
                  write(47,*) 'LINK'
                  link_di_title = .true.
                endif
                write(46,1006) nd2,nd1, 0,0, id1,id2,id3
                write(47,1006) nd2,nd1, 0,0, id1,id2,id3
              endif
              if (nd3.ne.0) write(46,1006) nd3,nd1, 0,0, id1,id2,id3
              if (nd4.ne.0) write(46,1006) nd4,nd1, 0,0, id1,id2,id3
              if (nd5.ne.0) write(46,1006) nd5,nd1, 0,0, id1,id2,id3
              if (nd6.ne.0) write(46,1006) nd6,nd1, 0,0, id1,id2,id3
              if (nd7.ne.0) write(46,1006) nd7,nd1, 0,0, id1,id2,id3
              if (nd8.ne.0) write(46,1006) nd8,nd1, 0,0, id1,id2,id3
              if (nd3.ne.0) write(47,1006) nd3,nd1, 0,0, id1,id2,id3
              if (nd4.ne.0) write(47,1006) nd4,nd1, 0,0, id1,id2,id3
              if (nd5.ne.0) write(47,1006) nd5,nd1, 0,0, id1,id2,id3
              if (nd6.ne.0) write(47,1006) nd6,nd1, 0,0, id1,id2,id3
              if (nd7.ne.0) write(47,1006) nd7,nd1, 0,0, id1,id2,id3
              if (nd8.ne.0) write(47,1006) nd8,nd1, 0,0, id1,id2,id3
              
            enddo     ! j
          enddo     ! i
        enddo     ! k 
      
        write(46,*)
        write(46,*)
        write(47,*)
        write(47,*)
      endif
      
      write(44,*)
      write(44,*)
      
c-----------------------------------------------------------------------
      
c     Setting lumen layer nodes for attaching new layer
      
      do k = 1,nnr       ! razina
        do j = 1,nnz-1      ! z smjer
          do i = 1,nnt-1    ! theta smjer
            if(elemmap(i,j,k).eq.0) then
              nodemap(9,i,j,k) = 0
              nodemap(9,i,j+1,k) = 0
              nodemap(9,i+1,j+1,k) = 0
              nodemap(9,i+1,j,k) = 0
            endif
          enddo     ! theta smjer
        enddo     ! z smjer
      enddo     ! razina     

c-----------------------------------------------------------------------

c     Write nodes in ilt lumen nodes field
      do j = 1,nnz
        do i = 1,nnt
          do k = 1,nnr
            nd = nodemap(1,i,j,k)
            if (nd.eq.0) then
              iltlumnodes(i,j) = nodemap(1,i,j,k-1)
              exit
            endif
          enddo
        enddo
      enddo
      
c-----------------------------------------------------------------------

c     Update node numbers in RLNOD field
      if (ilt_biochemo_flag.ge.2) then
        if (geometry_type.le.2) then
          do j = 1,nnz
            rlnod(1,j) = iltlumnodes(1,j)
          enddo
        elseif (geometry_type.eq.3) then
          do j = 1,nnz
            do i = 1,nnt
              rlnod(1,(i-1)*nnz+j) = iltlumnodes(i,j)
            enddo
          enddo
        endif
      elseif (export_surface_flag.eq.1) then
        if (geometry_type.eq.3) then
          do j = 1,nnz
            do i = 1,nnt
              rlnod(1,(i-1)*nnz+j) = iltlumnodes(i,j)
            enddo
          enddo
        endif
      endif
      
c-----------------------------------------------------------------------

c     Update wallkc_field
      if (zero_Kc_flag.eq.2) then
        do n = 1,wall_numel
          i = wallkc_field(2,n)
          j = wallkc_field(3,n)
          el = elemmap(i,j,1)
          if (el.eq.0) then
            wallkc_field(1,n) = 1
          else
            wallkc_field(1,n) = 0
          endif           
        enddo
      endif

c-----------------------------------------------------------------------
      
c     Based on number of new elements change numnp and numel
      numnp = node_number-1
      numel = press_elem_number -1
      
c     Decrease one tme step
      if (timfl) then
        ttim = ttim -dt
      endif
      
c     Reset counter for stepvise pressure addition
      ! prstep = 1
      
c     Close opened files     
      close(32)
      close(41)
      close(42)
      close(43)
      close(44)
      close(45)
      if (ilt_biochemo_flag.eq.3) then
        close(46)
        close(47)
      endif
      
1000  format(f6.3)
1001  format(i4)
1002  format(i9,i3,e16.8,e16.8,e16.8)
1003  format(i5,i3,i3,i8,i6,i6,i6,i6,i6,i6,i6)
1004  format(i9,i3,e16.8)
1005  format(i9,i3,i7,i5,i5)
1006  format(i7,i6,i3,i3,i5,i3,i3)
1007  format(a30)
3007  format(i5,i8,i5,i5)
      
      
c     Ispisi polja za provjeru
      
c      open(38,file='equations-mapp',status='replace',
c     &    action='write',form='formatted',position="append")
c      do i = 1,numnp
c        write(38,3007) i, id(1,i), id(2,i), id(3,i)
c      enddo
c      close(38)
      
c      open(31,file='mapping-'//finp(2:len_trim(finp)),status='replace',
c     &    action='write',form='formatted',position="append")
c      write(31,*) 'X polje'
c      do i=1,numnp
c          do j=1,ndm
c             write(31,1000) x(j,i)
c          enddo
c          write(31,*)
c      enddo
      
c      write(31,*)
c      write(31,*) 'IX polje'
      
c      do i=1,numel
c          do j=1,nen1
c             write(31,1001) ix(j,i)
c          enddo
c          write(31,*)
c      enddo
             
c      write(31,*)
c      write(31,*) 'U polje'
c      write(31,*)
c      do i=1,numnp
c          do j=1,ndf
c             write(31,'(f6.3)') u(j,i)
c          enddo
c          write(31,*)
c      enddo
            
c      write(31,*)
c      write(31,*) 'nodemap polje'
c      write(31,*)
c      do i=1,st
c          do j=1,sz
c             write(31,'(i4)') nodemap(i,j,1,1)
c          enddo
c          write(31,*)
c      enddo
      
c      write(31,*)
c      write(31,*) 'PRESSAP polje'
c      write(31,*)
c      do i=1,st-1
c          do j=1,sz-1
c             write(31,'(i4)') pressmap(i,j)
c          enddo
c          write(31,*)
c      enddo
      
c      write(31,*)
c      write(31,*) 'MAPADD polje'
c      write(31,*)
c      do i = 1,st-1
c        do j = 1,sz-1
c          write(31,'(l)') mapadd(i,j)
c        enddo
c        write(31,*)
c      enddo
      
c     close(31)
      
      end
