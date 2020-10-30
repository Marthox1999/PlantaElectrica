%Lectura
float: cN;
float: cH;
float: cT;
int: cpN;
int: cpH;
int: cpT;
int: n;
int: s;
array[int, int] of int : D;
float: rcH;
int: drA;

%Variables
array[1..n] of var int: pN;
array[1..n] of var int: pH;
array[1..n] of var int: pT;

%Var aux representa el dia maximo a tomar para
%calcular los dias consecutivos del regimen alto
var int: aux = n - drA + 1;

%Costo
var float: f;


%Restriccion de exceder capacidad
constraint forall(i in 1..n)(sum(j in 1..s)(D[j,i]) <= cpN+cpH+cpT);

%Restriccion de cumplir demanda
constraint forall(i in 1..n)(sum(j in 1..s)(D[j,i]) <= pN[i]+pH[i]+pT[i]);

%resticcion de regimen alto
constraint forall(i in 1..aux)(sum(k in i..i+drA-1)(pH[k] > cpH*rcH) < drA);

%Restricciones de capacidad
constraint forall(i in 1..n)(pN[i] <= cpN);
constraint forall(i in 1..n)(pH[i] <= cpH);
constraint forall(i in 1..n)(pT[i] <= cpT);

%Restricciones de no negatividad
constraint forall(i in 1..n)(pN[i] >= 0);
constraint forall(i in 1..n)(pH[i] >= 0);
constraint forall(i in 1..n)(pT[i] >= 0);

%Funcion Objetivo
constraint f = sum(i in 1..n)(pN[i]*cN + pH[i]*cH + pT[i]*cT );




solve minimize f;
output ["Produccion Nuclear=", show(pN), "\n Produccion Hidroelectrica=", show(pH), "\n Produccion Termica=", show(pT), "\n Costo=", show(f)];


