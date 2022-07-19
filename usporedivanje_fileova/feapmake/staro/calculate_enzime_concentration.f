      subroutine calculate_enzime_concentration(M_elas_history,
     &            M_MMP_history,mass)
      
      implicit none
      
      include 'num_method_parameters.h'
      include 'biochemo_parameters.h'
      include 'current_geometry.h'
      include 'comblk.h'
      include 'pointer.h'

      
      real(kind=8)  :: M_elas_history(1001), 
     &                 M_MMP_history(num_stored_steps), mass(23)
      real(kind=8)  :: ro, rip, rlum, rin, rl, M_MMP, M_elas, A_elas, 
     &                 A_MMP, B_elas, B_MMP, AVV_tot, ilt_thickness, 
     &                 M_elas_current, M_elas_initial, MEDP_tot, MN_tot
      real(kind=8), parameter :: zero=0d0, one=1d0, two=2d0
      logical :: run, stoper
      integer       :: k, s, i, j, sv, rd, t, n
      
c=======================================================================
c
c     Calculate current enzime concentrations for current increment and
c     save them into history field.
c
c     M_elas(r,s) --> current concentration of elastases in the IP
c     M_MMP(r,s)  --> current concentration of colagenases in the IP
c
c-----------------------------------------------------------------------

c     Current radii
      call outer_radius(hr(up(36)),hr(up(15)))
      call IP_radius(hr(up(15)))
      call lumen_radius(hr(up(37)),hr(up(15)))
      ro = rout_current       ! outer wall radius for current IP (radial projection)
      rip = rip_current       ! radius of current wall IP
      rlum = rlum_current     ! lumen radius for current IP (radial projection)
      rin = rin_current       ! inner wall radius for current IP (radial projection)
      
c     Determine radius of luminal biochemical surface
      ilt_thickness = rin - rlum
      if (ilt_thickness.lt.0.05) then
        rl = zero
        ilt_thickness = zero
      elseif(ilt_thickness.gt.2.0) then
        rl = rlum + 1.0
      else
        rl = rlum + 0.5*ilt_thickness
      endif
      
      if (ilt_thickness.gt.zero) then
      
c       Calculate total neutrofil concentration M^N_tot
        MN_tot = ilt_thickness / bio_layer_thickness * bio_MNi
        
c       Calculate total surface od vasa vasorum
        M_elas_initial = 0.125 * mass(23) * mass(6)
        M_elas_current = 0.125 * mass(23) * mass(13)
        MEDP_tot = bio_EDP_ratio * (M_elas_initial-M_elas_current)  ! ! ratio of EDP in total degraded elastin
        AVV_tot = bio_AVV_0 + bio_KVV_EDP * MEDP_tot    ! K^VV_EDP - correlation factor [mm^2_VV/g_M^EDP_tot]  
        
c       Calculate parameters A and B
        B_elas = bio_KN_elas * MN_tot
        B_MMP = bio_KN_MMP * MN_tot
        A_elas = (B_elas - bio_KVV_elas * AVV_tot) / dlog(rl/ro) 
        A_MMP = (B_MMP - bio_KVV_MMP * AVV_tot) / dlog(rl/ro)
        
c       Calculate concentrations
        M_elas = A_elas * dlog(rip/ro) + B_elas
        M_MMP = A_MMP * dlog(rip/ro) + B_MMP
        
      else
        M_elas = zero
        M_MMP = zero
      endif
      
c     Save values into history field
      M_elas_history(timestep) = M_elas
      M_MMP_history(history_save_index) = M_MMP      

c=======================================================================      
      end subroutine