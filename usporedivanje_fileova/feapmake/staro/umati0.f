c$Id:$
      subroutine umati0(type,vv, d, ud, n1,n3)

c      * * F E A P * * A Finite Element Analysis Program

c....  Copyright (c) 1984-2014: Regents of the University of California
c                               All rights reserved

c-----[--.----+----.----+----.-----------------------------------------]
c     Modification log                                Date (dd/mm/year)
c       Original version                                    01/11/2006
c-----[--.----+----.----+----.-----------------------------------------]
c      Purpose: Dummy user material model routine

c      Inputs:
c         type   - Name of material model
c         vv(5)  - Command line real data
c         d(*)   - Program material parameter data

c      Outputs:
c         ud(*)  - Material parameter data for model
c         n1     - Number of history items/point (time   dependent)
c         n3     - Number of history items/point (time independent)
c-----[--.----+----.----+----.-----------------------------------------]
      implicit  none
      
      include 'user_model_options.h'
      include 'geometric_parameters.h'
      include 'mesh_parameters.h'
      include 'homeostasis_parameters.h'
      include 'elastin_parameters.h'
      include 'collagen_parameters.h'
      include 'smc_parameters.h'
      include 'fiber_angles.h'
      include 'chem_parameters.h'
      include 'gain_rate_parameters.h'
      include 'flow_parameters.h'
      include 'AAA_parameters.h'
      include 'ilt_parameters.h'
      include 'num_method_parameters.h'
      include 'output_options.h'
      include 'time_parameters.h'
      include 'pconstant.h'
      include 'iofile.h'
      include 'growth_rate_calculation.h'
      include 'ilt_num_method_parameters.h'
      include 'user_ilt_flags.h'
      include 'fiber_dispersion.h'
      include 'FSG_parameters.h'

      logical   pcomp,errck,tinput
      character type*15, text(16)*16
      integer   n1,n3
      real*8    vv(5),d(*),ud(*),td(15),G_radial_elas,phi_coll, temp1

c     Set command name

      if(pcomp(type,'mat0',4)) then     ! Default  form DO NOT CHANGE
        type = 'maaa'                   ! Specify 'name'

c     Input user data and save in ud(*) array

      else                              ! Perform input for user data
          
c     Set value for number of history points
      n1 = 100
      
c     Save values from input file
      text(1) = 'xxxx'
      do while (.not.pcomp(text(1),'    ',4))
        errck  = tinput(text,1,td,15)
        
        if (pcomp(text(1),'flg1',4)) then 
            num_aaa_layers =        td(1)
            elas_prestretch_type =  td(2)
            elas_deg_option =       td(3)
            integration_type =      td(4)
            deviatoric_split =      td(5)
            growth_type =           td(6)
            coll_stiffening =       td(7)
            survival_type =         td(8)
            production_type =       td(9)
            geometry_type =         td(10)
            
        elseif (pcomp(text(1),'flg2',4)) then 
            sigma_active_model =    td(1)
            volumetric_type =       td(2)
            delta_sigma_type =      td(3)
            delta_c_type =          td(4)
            zeta_type =             td(5)
            ! change_basal =          td(6)
            basal_prod_model =      td(7)
            referent_timestep =     td(8)
            time_increments =       td(9)
            homeo_reload =          td(10)
            zero_Kc_flag =          td(11)
            turn_off_GR =          td(12)
            
        elseif (pcomp(text(1),'flg3',4)) then 
            smc_apoptosis =           td(1)
            Kc_modification =         td(2)
            fiber_orient_flag =       td(3)
            average_mass_flag =       td(4)
            hel_vector_symmetry =     td(5)
            Ksigma_modification =     td(6)
            centerline_flag =         td(7)
            fiber_I4_flag =           td(8)
            jacobian_flag =           td(9)
            fiber_break_flag =        td(10)
            reduce_smc_active_flag =  td(11)
            reduce_coll_prestretch =  td(12)
            fiber_switch_flag =       td(13)
            fourth_mat_flag =         td(14)
            
        elseif (pcomp(text(1),'flg4',4)) then 
            ilt_flag =              td(1)
            luminal_surface_flag =  td(2)
            if (nint(td(3)).eq.2) then
              move_pressure_flag = .true.
            endif
            ilt_boundary_flag =     td(4)
            ilt_elem_growth_flag =  td(5)
            ilt_volumetric_flag =   td(6)
            ilt_parameter_change =  td(7)
            ilt_element_rupture =   td(8)  
            ilt_inverseF_flag =     td(9)
            ilt_biochemo_flag =     td(10)
            operating_system_flag = td(11)
            
        elseif (pcomp(text(1),'flg5',4)) then 
            fiber_dispersion_flag = td(1)
            G_interpolation_flag =  td(2)
            kapa_mass_flag =        td(3)
            c2_calculation_flag =   td(4)
            kapa_radius_flag =      td(5)
            manual_G_flag =         td(6)
            if (fiber_dispersion_flag.eq.2) then
              c2_calculation_flag = 2
            else
              c2_calculation_flag = 1
            endif
            
        elseif (pcomp(text(1),'geom',4)) then 
            rin =             td(1)
            rout =            td(2)
            axial_length =    td(3)
            angle =           td(4)
            rmed =            td(5)
            radv =            td(6)
            vol_intima =      td(7)
            vol_media =       td(8)
            vol_adventitia =  td(9)
            width_transit =   td(10)
            
        elseif (pcomp(text(1),'mesh',4)) then 
            num_elem_r =      td(1) 
            num_elem_theta =  td(2) 
            num_elem_z =      td(3)
            wall_numel = num_elem_r * num_elem_theta * num_elem_z
            wall_numnl_with_pr = wall_numel + num_elem_theta*num_elem_z
            nnz = num_elem_z+1
            nnt = num_elem_theta+1
            
        elseif (pcomp(text(1),'home',4)) then 
            blood_press =     td(1)
            sig_homeo_aorta = td(2)
            sig_homeo_coll =  td(3)
            sig_homeo_smc =   td(4)

        elseif (pcomp(text(1),'ela1',4)) then 
            phi_elas =            td(1)
            phi_elas_int =        td(2)
            phi_elas_med =        td(3)
            phi_elas_adv =        td(4)
            G_theta_elas =        td(5)
            G_z_elas =            td(6)
            G_theta_elas_ri =     td(7)
            G_z_elas_ri =         td(8)
            G_theta_elas_ro =     td(9)
            G_z_elas_ro =         td(10)
            G_r_elas = G_radial_elas(G_theta_elas,G_z_elas)
            G_r_elas_ri = G_radial_elas(G_theta_elas_ri,G_z_elas_ri)
            G_r_elas_ro = G_radial_elas(G_theta_elas_ro,G_z_elas_ro)
            
        elseif (pcomp(text(1),'ela2',4)) then
            c1_elas =             td(1)
            K_index =             td(2)
            elas_half_life =      td(3)
            elas_half_life_deg =  td(4)
            elas_remaining =      td(5)
            elas_deg_start_step = nint(td(6))
            elas_deg_end_time =   td(7)
          
        elseif (pcomp(text(1),'col1',4)) then 
            c2_coll =         td(1)
            c3_coll =         td(2)
            c3_coll_max =     td(3)
            coll_prestretch = td(4)
            fiber_angle(1) =  td(5)
            fiber_angle(2) =  td(6)
            fiber_angle(3) =  td(7)
            fiber_angle(4) =  td(8)
            phi_coll_1 =      td(9)
            phi_coll_2 =      td(10)
            phi_coll_3 =      td(11)
            phi_coll_4 =      td(12)
            coll_prestretch0 = coll_prestretch
                     
        elseif (pcomp(text(1),'col2',4)) then 
            phi_coll_1_int =  td(1)
            phi_coll_2_int =  td(2)
            phi_coll_3_int =  td(3)
            phi_coll_4_int =  td(4)
            phi_coll_1_med =  td(5)
            phi_coll_2_med =  td(6)
            phi_coll_3_med =  td(7)
            phi_coll_4_med =  td(8)
            phi_coll_1_adv =  td(9)
            phi_coll_2_adv =  td(10)
            phi_coll_3_adv =  td(11)
            phi_coll_4_adv =  td(12)
            
        elseif (pcomp(text(1),'col3',4)) then 
            fiber_angle_dispersion(1) =  td(1)
            fiber_angle_dispersion(2) =  td(2)
            fiber_angle_dispersion(3) =  td(3)
            fiber_angle_dispersion(4) =  td(4)
            fiber_angle_dispersion(5) =  td(5)
            fiber_angle_dispersion(6) =  td(6)
            sigma_coll_critical =        td(7)
            G_coll_start_radius =        td(8)
            G_coll_end_radius =          td(9)
            G_coll_final =               td(10)
            
        elseif (pcomp(text(1),'smc1',4)) then 
            c2_smc =          td(1)
            c3_smc =          td(2)
            smc_prestretch =  td(3)
            fiber_angle(5) =  td(4)
            phi_smc =         td(5)
            phi_smc_int =     td(6)
            phi_smc_med =     td(7)
            phi_smc_adv =     td(8)
            
        elseif (pcomp(text(1),'smc2',4)) then   
            smc_TM =          td(1)
            smc_lambda_0 =    td(2)
            smc_lambda_M =    td(3)
            smc_K_active =    td(4)
            smc_beta_M =      td(5)
            TM_start_radius = td(6)
            TM_end_radius =   td(7)
            smc_TM0 = smc_TM
            
        elseif (pcomp(text(1),'chem',4)) then 
            C_basal =         td(1)
            Cs =              td(2)
            
        elseif (pcomp(text(1),'gain',4)) then   
            Kh_coll =         td(1)
            Kh_smc =          td(2)
            K_sigma_coll =    td(3)
            K_sigma_smc =     td(4)
            Kc_coll =         td(5)
            Kc_smc =          td(6)
            Kh_elas =         td(7)
            c3_zeta_coll =    td(8)
            c3_zeta_smc =     td(9)
            Kc_coll_modified = Kc_coll
            Kc_smc_modified = Kc_smc
            
        elseif (pcomp(text(1),'flow',4)) then   
            blood_density =     td(1)
            blood_viscosity =   td(2)
            homeostatic_WSS =   td(3)
            flow_perturb =      td(4)
            num_homeo_steps =   nint(td(5))
                  
        elseif (pcomp(text(1),'aaaa',4)) then   
            AAA_length =        td(1)
            AAA_half_length =   td(2)
            AAA_width =         td(3)
            Kc_homeo =          td(4)
            Kc_middle =         td(5)
            Kc_width =          td(6)
            Ksigma_homeo =      td(7)
            Ksigma_middle =     td(8)
            Ksigma_width =      td(9)
            sacc_width =        td(10)
            
        elseif (pcomp(text(1),'aaa2',4)) then   
            axial_deg_par1 =    td(1)
            axial_deg_par2 =    td(2)
            axial_deg_exp =     td(3)
            sacc_deg_par1 =     td(4)
            sacc_deg_exp =      td(5)
            
        elseif (pcomp(text(1),'num1',4)) then   
            augm_d1 =           td(1)
            augm_d1_initial =   td(1)
            num_stored_steps =  nint(td(2))
            tracking_node =     nint(td(3))
            dt2_d2t_factor =    td(4)
            Kc_mod_start =      nint(td(5))
            dr_dt_target =      td(6)
            num_ilt_layers =    td(7)
            ilt_elem_th =       td(8)
            req_distance =      td(9)
            
        elseif (pcomp(text(1),'num2',4)) then   
            delta_ilt_thickness = td(1)
            ilt_mat_num =         td(2)
            press_mat_num =       td(3)
            lum_surf_radius =     td(4)
            ilt_z_min =           td(5)
            ilt_z_max =           td(6)
            ilt_theta_min =       td(7)
            ilt_theta_max =       td(8)
            zero_press_mat_num =  td(9)
            ilt_mat_num_rupt =    td(10)
            end_lum_surf_radius = td(11)
            lum_surf_step_dist =  td(12)
            lum_surf_step_time =  td(13)
            nnr = num_ilt_layers+1
            ilt_numel = (nnt-1) * (nnz-1) * nnr
            
        elseif (pcomp(text(1),'num3',4)) then   
            TAWSS_boundary_value = td(1)

            
        elseif (pcomp(text(1),'out1',4)) then   
            output_1 =          nint(td(1))
            output_2 =          nint(td(2))
            output_3 =          nint(td(3))
            output_4 =          nint(td(4))
            output_5 =          nint(td(5))
            output_6 =          nint(td(6))
            output_7 =          nint(td(7))
            output_8 =          nint(td(8))
            output_9 =          nint(td(9))
            output_10 =         nint(td(10))
            output_11 =         nint(td(11))
            output_12 =         nint(td(12))
            
        elseif (pcomp(text(1),'out2',4)) then   
            output_node_1 =           nint(td(1))
            output_node_2 =           nint(td(2))
            output_node_3 =           nint(td(3))
            output_node_4 =           nint(td(4))
            output_node_5 =           nint(td(5))
            output_line_outer =       nint(td(6))
            output_line_inner =       nint(td(7))
            output_line_horizontal =  nint(td(8))
            output_line_middle =      nint(td(9))
            export_surface_flag =     nint(td(10))
            export_ronod_flag =       nint(td(11))
            export_y0_results =       nint(td(12))
            
        elseif (pcomp(text(1),'out3',4)) then   
            output_14 =         nint(td(1))
            output_15 =         nint(td(2))
            output_16 =         nint(td(3))
            output_17 =         nint(td(4))
            out_slice_num =     nint(td(5))
            out_slice_bottom =  td(6)
            out_slice_top =     td(7)
            if (out_slice_bottom.lt.0d0.or.
     &          out_slice_bottom.gt.axial_length) then
              out_slice_bottom = 0d0
              write(ilg,1002)
            endif
            if (out_slice_top.lt.0d0.or.
     &          out_slice_top.gt.axial_length) then
              out_slice_top = axial_length
              write(ilg,1003)
            endif
            if (out_slice_num.gt.nnz) then
              out_slice_num = nnz
              write(ilg,1004)
            endif
            
        elseif (pcomp(text(1),'time',4)) then   
            num_const_inc =     nint(td(1))
            max_increment =     td(2)
            min_increment =     td(3)
            time_3_const =      td(4)
            time_4_const =      td(5)
            
        elseif (pcomp(text(1),'fdis',4)) then   
            kapa_ip_one =           td(1)
            kapa_op_one =           td(2)
            kapa_ip_int =           td(3)
            kapa_ip_med =           td(4)
            kapa_ip_adv =           td(5)
            kapa_op_int =           td(6)
            kapa_op_med =           td(7)
            kapa_op_adv =           td(8)
            sigmoid_curvature_in =  td(9)
            sigmoid_curvature_out = td(10)
            kapa_ip_mass =          td(11)
            kapa_op_mass =          td(12)            
            kapa_ip = kapa_ip_one
            kapa_op = kapa_op_one
            
        elseif (pcomp(text(1),'fds2',4)) then   
            end_kapa_ip_one =     td(1)
            end_kapa_op_one =     td(2)
            end_kapa_ip_int =     td(3)
            end_kapa_ip_med =     td(4)
            end_kapa_ip_adv =     td(5)
            end_kapa_op_int =     td(6)
            end_kapa_op_med =     td(7)
            end_kapa_op_adv =     td(8)
            kapa_start_radius =   td(9)
            kapa_end_radius =     td(10)
            prestretch_Gm =       td(11)
            prestretch_Gp =       td(12)
            prestretch_Go =       td(13)
            
        endif
      end do
      
c     Maximum number of ILT elements
      max_num_ilt_elem = (nnt-1)*(nnz-1)*num_ilt_layers
      
c     Calculate homeostatic stretch for survival function
      if (fiber_dispersion_flag.ne.2) then
        call fiber_homeostatic_stretch()
      endif
      
c     Calculate homeostatic wall shear stress
c      if (referent_timestep.eq.1) then
c        tau_wall_homeo = (4d0 * blood_viscosity * 1d0) / 
c     &                    (pi * rin**3d0)
c      else
c        tau_wall_homeo = 0d0
c      endif
      
c     Adjust integration type
      if (time_increments.ne.1.and.integration_type.ne.2) then
        integration_type = 2
        write(ilg,1000)
        write(iow,1000)
      endif
      
c     Adjust options
      if (angle.lt.175d0.or.angle.gt.181d0) then
        centerline_flag = 1
      endif
      
c     Fiber dispersion check
      if (fiber_dispersion_flag.eq.2) then
        if (num_aaa_layers.eq.1.and.(phi_coll_1+phi_coll_2).ne.0d0) then
          write(ilg,1001)
          write(iow,1001)
        endif
        phi_coll = phi_coll_1_int + phi_coll_2_int + 
     &             phi_coll_1_med + phi_coll_2_med +
     &             phi_coll_1_adv + phi_coll_2_adv
        if (num_aaa_layers.eq.3.and.phi_coll.ne.0d0) then
          write(ilg,1001)
          write(iow,1001)
        endif
      endif
      
c     Counter reset
      fiber_break_counter = 0
      fiber_compressed_counter = 0
      
C     Flags
      tangent_zero = .false.
      
c     Adjust geometry_type flag
      if (ilt_biochemo_flag.eq.3) then
        geometry_type = 3
      endif
      
      endif
          
c-----------------------------------------------------------------------      
1000  format(/1x 'Integration type was changed to trapezoidal rule ',
     &      'with nonuniform time spacing.' /)
1001  format(/1x 'Fiber dispersion is implemented only for helical ',
     &  'collagen fiber. Set mass fraction of fibers 1 and 2 to zero.'/)
1002  format(/1x 'Warning: out_slice_bottom out of range'/)
1003  format(/1x 'Warning: out_slice_top out of range'/)
1004  format(/1x 'Warning: out_slice_num larger than axial number ',
     &           'of nodes'/)
c=======================================================================
      end
