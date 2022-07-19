      subroutine set_enzyme_concentration(M_elas_history,
     &            M_MMP_history,mass)
      
      implicit none
      
      include 'num_method_parameters.h'
      include 'biochemo_parameters.h'
      
      real(kind=8)  :: M_elas_history(1001), 
     &                 M_MMP_history(num_stored_steps), mass(2)
      
c=======================================================================
      
c     Save values into history field
      M_elas_history(timestep) = M_elas_ip
      M_MMP_history(history_save_index) = M_MMP_ip
      
c     Save values to mass field for GID output
      mass(1) = M_elas_ip
      mass(2) = M_MMP_ip

c=======================================================================      
      end subroutine