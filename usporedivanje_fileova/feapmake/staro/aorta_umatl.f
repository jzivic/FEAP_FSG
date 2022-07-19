c$Id:$
      subroutine aorta_umatl(f,finv,df,detf,be,ta,d,ntm,ii,istrt,sig,dd,
     &                xlamd,ha,isw,mass,production,survival,step_time,
     &                Gelas,history,growth,sigma_field,m_fiber,zetad,
     &                sigmaw,Q_polcart,kapa,biochemo_field,
     &                all_steps_time,ronod)


c      * * F E A P * * A Finite Element Analysis Program

c....  Copyright (c) 1984-2014: Regents of the University of California
c                               All rights reserved

c-----[--.----+----.----+----.-----------------------------------------]
c     Modification log                                Date (dd/mm/year)
c       Original version                                    01/11/2006
c-----[--.----+----.----+----.-----------------------------------------]
c     Purpose: User Constitutive Model 1

c     Input:
c          f(3,3)    - Deformation gradient
c          finv(3,3) - Inverse deformation gradient
c          df(3,3)   - Incremental deformation gradient
c          detf      - Determinant of deformation gradient
c          be(6)     - Left Cauchy-Green tensor
c          ta        - Temperature change
c          d(*)      - Program material parameters (ndd)
c          ud(*)     - User material parameters (nud)
c          hn(nh)    - History terms at point: t_n
c          h1(nh)    - History terms at point: t_n+1
c          nh        - Number of history terms
c          ntm       - Number of stress components
c          ii        - Point being processed
c          istrt     - Start state: 0 = elastic; 1 = last solution
c          isw       - Solution option from element

c     Output:
c          sig(*)  -  Stresses at point.
c                     N.B. 1-d models use only sig(1)
c          dd(6,*) -  Current material tangent moduli
c                     N.B. 1-d models use only dd(1,1) and dd(2,1)
c-----[--.----+----.----+----.-----------------------------------------]

c     Compute and output stress (sig) and (moduli) for integration point

      implicit none
      
      include 'elaugm.h'    ! elamd, eha
      include 'elcoor.h'    ! xref, xcur
      include 'counts.h'    ! niter, naugm
      include 'tdata.h'
      include 'eldata.h'
      include 'num_method_parameters.h'
      include 'data_print.h'
      include 'user_model_options.h'
      include 'output_options.h'
      include 'comblk.h'
      include 'pointer.h'
      include 'tangent.h'
      include 'fiber_dispersion.h'
      include 'field_initialization_flags.h'
      include 'ilt_num_method_parameters.h'
      
c	Feap variables
      integer   ntm,istrt,isw,ii
      real*8    ta,xlamd,ha
      real*8    f(3,3),finv(3,3),df(3,3),detf,be(6),
     &          d(*), sig(6),dd(6,6)

c     User variables
      ! Parameters
      real(kind=8), parameter :: zero=0d0, one=1d0

      ! Counters
      integer   i, j, k
      
      ! Stress and tangent moduli
      real*8    sig_elas(6), sig_fiber(6), sig_smc_act(6), sig_vol(6)
      real*8    dd_elas(6,6), dd_fiber(6,6), dd_smc_act(6,6),dd_vol(6,6)
      real*8    sigmaw(18), detfe
     
      ! History field
      real*8    history(63,num_stored_steps)

      ! Elastin
      real*8    Gelas(5), Ge(3,3), D_elas(3,3), Fn0_elas(3,3), 
     &          bn0_elas(3,3), Cn0_elas(3,3), finvtaue(3,3)
     
      ! Fibers
      real*8    Fn0_fiber(3,3,5), D_fiber(3,3), M(3,3,5), M0(3,3,5), 
     &          Gf(3,3,5), Gf0(3,3,5), m_fiber(3,11), sigma_field(21), 
     &          smc(6), MM(3,3), finvtauf(3,3)
     
      ! Tensors
      real*8    Ce(3,3), Fg(3,3), Fg_1(3,3), Aux(3,3), K_tensor(3,3,6),
     &          sigma(3,3), ff(3,3)
      real*8    j13
     
      ! Invariants
      real*8    I1, matrix_trace
     
      ! Mass calculation
      real*8    mass(23), production(num_stored_steps,5), 
     &          survival(num_stored_steps+1,5),
     &          step_time(num_stored_steps),
     &          growth(3,3,2), zetad(6)
     
      ! Transformation matrix
      real*8    Q_polcart(8)
      
      ! Fiber dispersion
      real*8    kapa(4)
      
      ! Biochemical moedel
      real*8    biochemo_field(1001+num_stored_steps),
     &          all_steps_time(1000), ronod(11,*)

c=======================================================================     

c     Calculate Global Transformation Matrix
      call Q_polar_to_cartesian(Q_polcart)
      
c     Determine current inner radius
      if (geometry_type.ne.1) then
        call inner_radius(hr(up(10)),hr(up(15)))
      endif
      
c     Calculate modified c3 parameter for collagen axial fibers
      call collagen_c3_parameter()
      
c     Initialize kczer field
      if (ilt_flag.eq.2.and.zero_Kc_flag.eq.2.and.
     &   (.not.kczer_initialized).and.ii.eq.1) then
          call initialize_kczer_field(mr(up(31)),mr(up(16)),hr(np(43)))
      endif
        
c-----------------------------------------------------------------------       
c     CALCULATE KAPA PARAMETERS
      
      if (fiber_dispersion_flag.eq.2) then
        ! no kapa change with radius
        if (kapa_radius_flag.eq.1) then
          if (timestep.eq.1) then
            if (num_aaa_layers.eq.1) then 
              kapa(1) = kapa_ip_one
              kapa(2) = kapa_op_one
              kapa(3) = kapa_ip_one
              kapa(4) = kapa_op_one
              kapa_ip = kapa_ip_one
              kapa_op = kapa_op_one
            elseif (num_aaa_layers.eq.3) then
              call kapa_parameters(xref)
              kapa(1) = kapa_ip
              kapa(2) = kapa_op
              kapa(3) = kapa_ip
              kapa(4) = kapa_op
            endif
          else ! (timestep>1)
            kapa_ip = kapa(3)
            kapa_op = kapa(4)
          endif
          
        ! kapa change with radius
        elseif (kapa_radius_flag.eq.2) then
          ! first timestep
          if (timestep.eq.1) then
            if (num_aaa_layers.eq.1) then 
              kapa(1) = kapa_ip_one
              kapa(2) = kapa_op_one
              kapa(3) = kapa_ip_one
              kapa(4) = kapa_op_one
              kapa_ip = kapa_ip_one
              kapa_op = kapa_op_one
            elseif (num_aaa_layers.eq.3) then
              call kapa_parameters(xref)
              kapa(1) = kapa_ip
              kapa(2) = kapa_op
              kapa(3) = kapa_ip
              kapa(4) = kapa_op
            endif
            
          else ! (timestep>1)
            call modify_kapa_with_radius(xref)
            kapa(3) = kapa_ip
            kapa(4) = kapa_op
                  
          endif
        endif  
      endif
        
c-----------------------------------------------------------------------       
c     MODIFY TM and COLLAGEN PRESTRETCH
      if (reduce_smc_active_flag.eq.2) then
        call modify_TM()  
      endif
      
      if (reduce_coll_prestretch.eq.2) then
        call modify_coll_prestretch()  
      endif
      
c----------------------------------------------------------------------- 
c     CALCULATE CONSTITUENTS MASS
      
      if (niter.eq.0.and.naugm.eq.0) then
	  ! -- First newton and augmented iteratio. --
        ! -- Mass is calculated in first iteration and stored in memory 
        ! for use in later iteratons. --
      
        if (timestep.eq.1) then   ! ttim = 0
          call calculate_initial_mass(mass(1:7),xref)
          call calculate_elastin_prestretch(Gelas,xref)
          call elastin_zeta_denominator(Gelas)
          call calculate_element_real_mass(mass(23),n,hr(np(43)),
     &          mr(np(33)))
        endif
        
        ! Production
        call calculate_basal_production(mass,step_time)
        if (timestep.eq.1) then
          call dlaset('A',3,3,zero,one,Fg,3)
        else
          call growth_tensor(mass(14),Fg,m_fiber)
        endif
        ff = f
        if (volumetric_type.eq.1) then
          call dgemm('N','N',3,3,3,one, f ,3, Fg ,3,zero, ff, 3)
        endif
        call calculate_fiber_vector(m_fiber,ff,
     &                        history(55:63,previous_step_index),xref)
        call calculate_mass_production(mass,production,
     &                          sigma_field,sigmaw(13:18),m_fiber)
        call fiber_structural_tensor_M(m_fiber,M)
     
        ! Fiber homeostatic stretch
        if (fiber_dispersion_flag.eq.2.and.timestep.eq.1) then
          call fiber_prestretch_tensor(M,Gf,m_fiber)
          call fiber_zeta_denominator(M,Gf)
          zetad(1:5) = zeta_denominator(1:5)
        endif
        
        ! Survival function
        if (timestep.gt.1) then
          if (fiber_dispersion_flag.eq.2) then
            zeta_denominator(1:5) = zetad(1:5)
          endif
          zeta_denominator(6) = Gelas(4)
          !call growth_tensor(mass(14),Fg,m_fiber) ! mass is from step before
          call tensor_invers(Fg,Fg_1)
          call elastin_prestretch_tensor(Gelas,Ge)
          call dgemm('N','N',3,3,3,one, Fg ,3, Ge ,3,zero, D_elas, 3)
          call dgemm('N','N',3,3,3,one, f ,3, D_elas,3,zero, Fn0_elas,3)
          call dgemm('N','N',3,3,3,one, f ,3, Fg ,3,zero, Aux, 3)
          call save_F_tensor(Aux,history(55,history_save_index))
          
          ! ILT biochemical influence
          if (ilt_biochemo_flag.eq.2) then
            call calculate_enzime_concentration(biochemo_field(1),
     &            biochemo_field(1002),mass)
          elseif(ilt_biochemo_flag.eq.3) then
            call set_enzyme_concentration(biochemo_field(1),
     &           biochemo_field(1002))
          endif
          
          call calculate_survival_function(survival,step_time,M,f,Fg,
     &                        history,Fn0_elas,Gelas(5),m_fiber,ttim,
     &                        biochemo_field(1),biochemo_field(1002),
     &                        all_steps_time)
        endif
        
        ! Current mass
        call calculate_current_mass(mass,production,survival,step_time,
     &                              Gelas(5))
 
     
        ! Write elastin mass to ronod field
        if(isw.eq.3.and.ilt_biochemo_flag.ge.2.and.
     &     modfeap_number.ne.0) then
          call save_elastin_mass_ronod(ronod,mass)
        endif
     
        ! Growth tensor with current mass
        call growth_tensor(mass(14),Fg,m_fiber)
        call tensor_invers(Fg,Fg_1)
        growth(:,:,1) = Fg
        growth(:,:,2) = Fg_1
        
        if(kapa_mass_flag.gt.1.and.timestep.gt.1) then
          call modify_kapa_due_to_mass(kapa,mass)
        endif
        
      endif ! (niter.eq.0.and.naugm.eq.0)
        
c-----------------------------------------------------------------------         
c     CALCULATE CURRENT VALUES 
      
      ! Right Cauchy-Green tensor [Ce] - C(s) = F(s)^T * F(s)
      call dgemm('T','N',3,3,3,one, f ,3, f ,3,zero, Ce, 3)
      
      ! Growth tensor [Fg] - Fg(s) and invers of growth tensor [Fg_1] - Fg^-1(s)
      if (niter.ne.0.or.naugm.ne.0) then
        Fg = growth(:,:,1)
        Fg_1 = growth(:,:,2)
      endif
      
      ! -- inv(F) - used as F^-1(tau) in later increments --
      if (jacobian_flag.eq.2) then
        detfe = detf / mass(14)
      else
        detfe = detf
      endif
      j13 = detfe**(1d0/3d0)
      if (deviatoric_split.eq.1) then
        finvtaue = finv
        finvtauf = finv
      elseif (deviatoric_split.eq.2) then
        finvtaue = j13 * finv
        finvtauf = finv
      elseif (deviatoric_split.eq.3) then
        finvtaue = finv
        finvtauf = j13 * finv
      elseif (deviatoric_split.eq.4) then
        finvtaue = j13 * finv
        finvtauf = j13 * finv
      endif        
      
      ! -- E l a s t i n --
      
      ! Elastin prestretch tensor [Ge]
      call elastin_prestretch_tensor(Gelas,Ge)
      
      ! Auxiliary tensor [D_elas] - D = Fg(s) * G(0)
      call dgemm('N','N',3,3,3,one, Fg ,3, Ge ,3,zero, D_elas, 3)
      
      ! Deformation gradient tensor [Fn0_elas] - Fn0 = F(s) * D_elas
      call dgemm('N','N',3,3,3,one, f ,3, D_elas ,3,zero, Fn0_elas, 3)
      
      ! Left Cauchy-Green tensor [bn0_elas] - bn(0) = Fn(0) * Fn(0)^T
      call dgemm('N','T',3,3,3,one, Fn0_elas ,3, Fn0_elas ,3,zero, 
     &           bn0_elas, 3)
      
      ! I1 invariant      
      call dgemm('T','N',3,3,3,one, Fn0_elas ,3, Fn0_elas ,3,zero, 
     &           Cn0_elas, 3)
      I1 = matrix_trace(Cn0_elas,3)
      
      ! Auxiliary tensor [K_tensor] - K_k(tau)
      call dgemm('N','N',3,3,3,one, Fg_1 ,3, finvtaue ,3,zero, Aux, 3)
      call dgemm('N','N',3,3,3,one, Aux ,3, Ge ,3,zero, 
     &              K_tensor(1,1,6), 3)
      
      ! -- F i b e r s --
      
      
      !if (niter.ne.0.or.naugm.ne.0) then
      ! m_fiber
      if (.not.(timestep.ne.1.and.fiber_orient_flag.eq.2)) then
        ff = f
        if (volumetric_type.eq.1) then
          call dgemm('N','N',3,3,3,one, f ,3, Fg ,3,zero, ff, 3)
        endif
        call calculate_fiber_vector(m_fiber,ff,
     &       history(55:63,previous_step_index),xref)
      endif
      
      ! [M] - M_k(s)
      call fiber_structural_tensor_M(m_fiber,M)
      !endif
        
      !-----------------------------      
      if (fiber_I4_flag.eq.2) then
        
        ! Fiber prestretch tensor [Gf] - G_k(s)
        call fiber_prestretch_tensor(M,Gf,m_fiber)
        
        ! Fiber prestretch tensor [Gf0] - G_k(0)
        do k = kk,5
          call dgemm('N','N',3,3,1,one,m_fiber(1,k+5),3,m_fiber(1,k+5),
     &            1,zero, M0(1,1,k), 3)
     
          if (fiber_dispersion_flag.eq.2.and.(k.eq.3.or.k.eq.4)) then
            call generalized_structure_tensor(m_fiber(1,5+3),
     &            m_fiber(1,5+4),M0(1,1,k))
          endif
          
        enddo
        call fiber_prestretch_tensor(M0,Gf0,m_fiber(1,6))
        
        ! Deformatio gradient tensor [Fn0_fiber]
        do k = kk,5
          call dgemm('N','N',3,3,3,one, Fg ,3, Gf0(1,1,k) ,3,zero, 
     &               D_fiber, 3)
          call dgemm('N','N',3,3,3,one, f ,3, D_fiber ,3,zero, 
     &               Fn0_fiber(1,1,k), 3)    
        enddo
        
        ! Auxiliary tensor [K_tensor] - K_k(tau)
        do k = kk,5
          call dgemm('N','N',3,3,3,one, Fg_1 ,3, finvtauf ,3,zero,Aux,3)
          call dgemm('N','N',3,3,3,one, Aux ,3, Gf(1,1,k) ,3,zero, 
     &                K_tensor(1,1,k), 3)
        enddo
      
      !----------------------------- 
      else
        
        ! Fiber prestretch tensor [Gf] - G_k(s)
        call fiber_prestretch_tensor(M,Gf,m_fiber)
        
        ! Deformatio gradient tensor [Fn0_fiber]
        do k = kk,5
          call dgemm('N','N',3,3,3,one, Fg ,3, Gf(1,1,k) ,3,zero, 
     &               D_fiber, 3)
          call dgemm('N','N',3,3,3,one, f ,3, D_fiber ,3,zero, 
     &               Fn0_fiber(1,1,k), 3)    
        enddo
        
        ! Auxiliary tensor [K_tensor] - K_k(s)
        do k = kk,5
          call dgemm('N','N',3,3,3,one, Fg_1 ,3, finvtauf ,3,zero,Aux,3)
          call dgemm('N','N',3,3,3,one, Aux ,3, Gf(1,1,k) ,3,zero, 
     &                K_tensor(1,1,k), 3)
        enddo
 
      endif ! sigma_I4_flag
      
c-----------------------------------------------------------------------
c     SAVE CURRENT VALUES TO HISTORY
      
      ! Auxiliary tensor [K_tensor] - K_k(tau)
      call save_K_tensor(K_tensor,history(1,history_save_index))
      
      ! Deformation gradient - F0s
      call dgemm('N','N',3,3,3,one, f ,3, Fg ,3,zero, Aux, 3)
      call save_F_tensor(Aux,history(55,history_save_index))

c-----------------------------------------------------------------------      
c     CALCULATE CONSTITUENTS STRESS (sig) and TANGENT MODULI (dd)
      
      ! Elastin
      call sigma_elastin(sig_elas,mass,detf,bn0_elas,I1)
      call tangent_moduli_elastin(dd_elas,mass,detf,bn0_elas,I1)
      
      ! Collagen fiber and SMC passive part     
      call sigma_fiber(sig_fiber,dd_fiber,f,detf,Fg,Fn0_fiber,M,mass,
     &    production,survival,step_time,history,sigma_field,smc,m_fiber)
     
      ! SMC active part
      call smc_active(sig_smc_act,dd_smc_act,M(1,1,5),mass,
     &                m_fiber(1,5),step_time,survival(1,5),
     &                production(1,5),history,f,Fg,sigma_field)
      
      ! Volumetric part - Augmented Lagrange update
      call sigma_volumetric(sig_vol,mass,detf,xlamd,ha)
      call tangent_moduli_volumetric(dd_vol,mass,detf,xlamd)
      
      ! Total current stress and tangent moduli
      !sig = smc + sig_smc_act
      sig = sig_elas + sig_fiber + sig_smc_act + sig_vol 
      dd = dd_elas + dd_fiber + dd_smc_act + dd_vol
      
      ! Modify tangent moduli to increase stability
      if (tangent_flag) then
        dd = tangent_factor * dd
      endif

c----------------------------------------------------------------------- 
      ! Save stress for delta_sigma calculation
      if (delta_sigma_type.eq.2.or.delta_sigma_type.eq.4) then
        if (timestep.le.3) then
          call voight_to_matrix(sig,sigma)      
          do k = kk,5
            call dgemm('N','N',3,3,1,one, m_fiber(1,k) ,3, m_fiber(1,k),
     &              1,zero, MM, 3)
            call dgemm('T','N',3,3,3,one,MM,3,sigma,3,zero,Aux,3)
            !call dgemm('T','N',3,3,3,one,M(:,:,k),3,sigma,3,zero,Aux,3)
            sigma_field(k) = matrix_trace(Aux,3)
          enddo
        endif
        sigma_field(6:11) = sig
      endif
      
c-----------------------------------------------------------------------      
c     SAVE DATA FOR OUTPUT
      
      if (n.eq.1.and.ii.eq.1) then
        mass14 = mass(14)
        Jacobi = detf
        kapa_ip11 = kapa_ip
        kapa_op11 = kapa_op
      endif
      
      if (n.eq.output_node_5) then
        detS = sig(1) * (sig(2)*sig(3) - sig(5)*sig(5)) - 
     &         sig(4) * (sig(4)*sig(3) - sig(5)*sig(6)) +
     &         sig(6) * (sig(4)*sig(5) - sig(2)*sig(6))
        J_detS = detf / detS 
        
        sferni_dio = (sig(1)+sig(2)+sig(3))/3d0
        
      endif
      
      mass(20) = detf
      sigmaw(1:6) = sig_vol
      sigmaw(7:12) = sig_smc_act
      
c=======================================================================
      end
