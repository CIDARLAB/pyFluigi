DEVICE mix



LAYER FLOW 

MIXER mixer_1 ;
PORT port_1 ;
PORT port_2 ;



CHANNEL channel_1 from mixer_1 2 to port_1 1  ;
CHANNEL channel_2 from port_2 1 to mixer_1 1  ;

 

END LAYER

