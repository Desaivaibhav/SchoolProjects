/*
1)We first imported CSV data into SAS
2)Ran regression only for independent variables commercial and NGO
3)We check correlation between control variables
4)Run Principal component analysis and select 5 factors (closest to 85%)
5)Ran principal component method via Proc factor with nfacor=5
6)Ran regression for different models
	a)Model with only the principal components
	b)Model with only the principal components and Comm_Entrp_IV
	c)Model with  the principal components and NGO_IV
	d)Model with  the principal components, Comm_Entrp_IV, NGO_IV
*/

/*give the reference path*/
proc import datafile="C:\submission\soc_dat.csv" out=soc_data dbms=csv replace;
run;

title "Regression of Socio_Entrp vs Comm_Entrp_IV NGO_IV";
proc reg data=soc_data ;
 model Socio_Entrp= Comm_Entrp_IV NGO_IV  /stb ;
run;
title "Correlation between control variables";
proc corr data=soc_data ;
 var Financing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics  Int_markt_openness  Phy_serv_Infra  Cult_Social_norms;
run;
title "Standardize variables";
proc standard data=soc_data mean=0 std=1 out=soc_data_z ;
 var Financing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics  Int_markt_openness  Phy_serv_Infra  Cult_Social_norms;
run;

title "Variable reduction using principal compnent method";
Proc factor data=soc_data_z method=principal scree ;
var Financing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics  Int_markt_openness  Phy_serv_Infra  Cult_Social_norms;
run;

title "Factor anaysis with 5 factors and varimax rotation ";
Proc factor data=soc_data_z method=principal nfactor=5  rotate=varimax scree out=Social_data_factors_z;
var Financing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics  Int_markt_openness  Phy_serv_Infra  Cult_Social_norms;
run;

data Social_data_factors_z;
rename Factor1=Gov_RD_Support
Factor2=Market_infrastructure
Factor3=Institutional_Support
Factor4=Post_entrp_training_Comp
Factor5=int_mark_dynamics_comp;
set Social_data_factors_z;
run;
title "Model with only the principal components"; 
proc reg data=Social_data_factors_z ;
 model Socio_Entrp=   Gov_RD_Support Market_infrastructure Institutional_Support 
Post_entrp_training_Comp int_mark_dynamics_comp/vif ;
run;
title "Model with only the principal components and Comm_Entrp_IV"; 
proc reg data=Social_data_factors_z ;
 model Socio_Entrp= Comm_Entrp_IV  Gov_RD_Support Market_infrastructure Institutional_Support 
Post_entrp_training_Comp int_mark_dynamics_comp/vif ;
run;

title "Model with only the principal components and NGO_IV"; 
proc reg data=Social_data_factors_z ;
 model Socio_Entrp= NGO_IV  Gov_RD_Support Market_infrastructure Institutional_Support 
Post_entrp_training_Comp int_mark_dynamics_comp/vif ;
run;
title "Model with  the principal components, Comm_Entrp_IV, NGO_IV"; 
proc reg data=Social_data_factors_z ;
 model Socio_Entrp= NGO_IV Comm_Entrp_IV Gov_RD_Support Market_infrastructure Institutional_Support 
Post_entrp_training_Comp int_mark_dynamics_comp/vif ;
run;


/*------------------------------xxxxxxxxxxxxxxxxxxxx------------------------------

Proc factor data=soc_data_z method=principal nfactor=5  rotate=varimax scree out=Social_data_factors_z;
var Financing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics  Int_markt_openness  Phy_serv_Infra  Cult_Social_norms;
run;

data Social_data_factors_z;
rename Factor1=Gov_RD_Support
Factor2=Market_infrastructure
Factor3=Institutional_Support
Factor4=Post_entrp_training_Comp
Factor5=int_mark_dynamics_comp;
set Social_data_factors;
run;
title "Model with only the principal components"; 
proc reg data=Social_data_factors_z ;
 model Socio_Entrp=   Gov_RD_Support Market_infrastrucure Institutional_Support 
Post_entrp_training_Comp int_mark_dynamics_comp/vif ;
run;
title "Model with only the principal components and Comm_Entrp_IV"; 
proc reg data=Social_data_factors ;
 model Socio_Entrp= Comm_Entrp_IV  Gov_RD_Support Market_infrastrucure Institutional_Support 
Post_entrp_training_Comp int_mark_dynamics_comp/vif ;
run;

title "Model with only the principal components and NGO_IV"; 
proc reg data=Social_data_factors ;
 model Socio_Entrp= NGO_IV  Gov_RD_Support Market_infrastrucure Institutional_Support 
Post_entrp_training_Comp int_mark_dynamics_comp/vif ;
run;
title "Model with  the principal components, Comm_Entrp_IV, NGO_IV"; 
proc reg data=Social_data_factors_z ;
 model Socio_Entrp= NGO_IV Comm_Entrp_IV Gov_RD_Support Market_infrastrucure Institutional_Support 
Post_entrp_training_Comp int_mark_dynamics_comp/vif ;
run;

proc reg data=Social_data_factors ;
 model Socio_Entrp= NGO_IV Comm_Entrp_IV Gov_RD_Support Market_infrastrucure Institutional_Support 
Post_entrp_training_Comp int_mark_dynamics_comp/vif ;
run;


proc reg data=soc_data ;
 model Socio_Entrp= Fianancing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics  Int_markt_openness  Phy_serv_Infra  Cult_Social_norms Region1 Region2 Region3 Region4 Region5;;
run;
proc reg data=Social_entrp_data_fact ;
 model Socio_Entrp=  Fianancing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics 
Int_markt_openness  Phy_serv_Infra  Cult_Social_norms/ selection=stepwise;
run;

proc reg data=Social_entrp_data ;
 model Socio_Entrp= Post_entrp_training Region1 Region2 Region3 Region4 Region5 Region6 Region7;
run;

proc reg data=Social_entrp_data ;
 model Socio_Entrp=  comm_entrp_IV Post_entrp_training Region1 Region2 Region3 Region4 Region5 Region6 Region7;
run;

proc sort data=Social_entrp_data_region out=Social_entrp_data_region_sort;
by Region_code;
run;
proc reg data=data ;
by Region;
 model Socio_Entrp=  NGO_IV comm_entrp_IV ;
run;

/***------------------------------------
DATA Social_entrp_data;
     SET soc_data;
IF Region="USA" then Region1=1; ELSE Region1 = 0;
IF Region="Eastern Europe" then Region2=1; ELSE Region2 = 0;
IF Region="Latin America" then Region3=1; ELSE Region3 = 0;
IF Region="Southeast Asia" then Region4=1; ELSE Region4 = 0;
IF Region="MENA" then Region5=1; ELSE Region5 = 0;
IF Region="Caribbean" then Region6=1; ELSE Region6 = 0;
IF Region="Africa" then Region7=1; ELSE Region7 = 0;
run;
DATA Social_entrp_data_region;
     SET Social_entrp_data_fact;
IF Region="USA" then Region_code=1; 
IF Region="Eastern Europe" then Region_code=2; 
IF Region="Western Europe" then Region_code=3; 
IF Region="Latin America" then Region_code=4; 
IF Region="Southeast Asia" then Region_code=5; 
IF Region="MENA" then Region_code=6; 
IF Region="Caribbean" then Region_code=7; 
IF Region="Africa" then Region_code=8; 
run;


proc reg data=Social_entrp_data ;
 model Socio_Entrp= Region1 Region2 Region3 Region4 Region5 Region6 Region7;
run;
*/
/*
proc reg data=Social_entrp_data ;
 model Socio_Entrp= Fianancing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics  Int_markt_openness  Phy_serv_Infra  Cult_Social_norms Region1 Region2 Region3 Region4 Region5;
run;


Proc corr data=Social_entrp_data ;
var  Fianancing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics  Int_markt_openness  Phy_serv_Infra  Cult_Social_norms Region1 Region2 Region3 Region4 Region5 Region6 Region7;
run;

Proc princomp data=Social_entrp_data ;
var  Fianancing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics  Int_markt_openness  Phy_serv_Infra  Cult_Social_norms;
run;
Proc factor data=Social_entrp_data method=principal nfactor=5  rotate=varimax scree out=Social_entrp_data_fact;
var Fianancing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics  Int_markt_openness  Phy_serv_Infra  Cult_Social_norms;
run;


proc reg data=Social_entrp_data_fact ;
 model Socio_Entrp=  ngo_IV comm_entrp_IV Factor1 Factor2  Factor3 Factor4 Factor5 ;
run;

proc reg data=Social_entrp_data_fact ;
 model Socio_Entrp= ngo_IV comm_entrp_IV Factor1  Region4 ;
run;

proc reg data=Social_entrp_data_fact ;
 model Socio_Entrp= ngo_IV comm_entrp_IV Factor1  Region4 ;
run;


proc reg data=Social_entrp_data_fact ;
 model Socio_Entrp= ngo_IV comm_entrp_IV Fianancing  Govt_support  Tax_bureaucracy  Gov_program  Basic_entrp_training  Post_entrp_training  RD  Comm_prof_infra  int_mark_dynamics 
Int_markt_openness  Phy_serv_Infra  Cult_Social_norms 
Region1 Region2 Region3 Region4 Region5 Region6 Region7 ;
run;


proc reg data=Social_entrp_data_fact ;
 model Socio_Entrp=  ngo_IV comm_entrp_IV Factor1 Factor2  Factor3 Factor4 Factor5
Region1 Region2 Region3 Region4 Region5 Region6 Region7 /vif ;
run;


proc reg data=Social_entrp_data_fact ;
  


run;
*/


