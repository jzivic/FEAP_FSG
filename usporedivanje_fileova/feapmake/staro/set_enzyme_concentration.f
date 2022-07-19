      subroutine set_enzyme_concentration(M_elas_history,
     &            M_MMP_history)
      
      implicit none
      
      include 'num_method_parameters.h'
      include 'biochemo_parameters.h'
      
      real(kind=8)  :: M_elas_history(1001), 
     &                 M_MMP_history(num_stored_steps)
      
c=======================================================================
      
c     Save values into history field
      M_elas_history(timestep) = M_elas_ip
      M_MMP_history(history_save_index) = M_MMP_ip      

c=======================================================================      
      end subroutine