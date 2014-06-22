##### Program
# Sets
set vertex_v;
set edge_v within {vertex_v,vertex_v};
set vertex_s;
set edge_s within {vertex_s,vertex_s};

# Params
param c_v {vertex_s} >= 0;
param c_e {edge_s} >= 0;
param d_v {vertex_v} >= 0;
param d_e {edge_v} >= 0;

# Variables
var a {edge_s} >= 0;
var b {edge_v, vertex_s} binary;
var r {vertex_s, vertex_v} binary;
var l {edge_s, edge_v} binary;
var N {edge_v, vertex_s} binary;

# Objective Function
minimize total_band:
	sum {(e1,e2) in edge_s} a[e1,e2];
	
# Constraints
subject to S1 {v_s in vertex_s}:
	sum {v_v in vertex_v} r[v_s, v_v] <= 1;
subject to S2 {v_v in vertex_v}:
	sum {v_s in vertex_s} r[v_s, v_v] = 1;
subject to S3 {v_s in vertex_s, v_v in vertex_v}:
	r[v_s, v_v] * d_v[v_v] <= c_v[v_s];
subject to S4 {(e1,e2) in edge_s}:
	a[e1,e2] = sum {(e_v1,e_v2) in edge_v} d_e[e_v1,e_v2] * l[e1,e2, e_v1,e_v2];
subject to S5 {(e_v1,e_v2) in edge_v}:
	sum {(e1,e2) in edge_s} l[e1,e2, e_v1,e_v2] >= 1;
subject to S6 {(e_s1,e_s2) in edge_s}:
	a[e_s1,e_s2] <= c_e[e_s1,e_s2];
subject to S7 {(v1_v, v2_v) in edge_v, v1_s in vertex_s}:
	r[v1_s, v1_v] <= sum {(v_s1,v_s2) in edge_s: v1_s = v_s1 or v_s2 = v1_s} l[v_s1,v_s2, v1_v,v2_v];
subject to S8 {(v1_v, v2_v) in edge_v, v1_s in vertex_s}:
	r[v1_s, v2_v] <= sum {(v_s1,v_s2) in edge_s: v1_s = v_s1 or v_s2 = v1_s} l[v_s1,v_s2, v1_v,v2_v];
subject to S9 {(v1_v, v2_v) in edge_v, v_s in vertex_s}:
	r[v_s, v1_v] <= b[v1_v, v2_v, v_s];
subject to S10 {(v1_v, v2_v) in edge_v, v_s in vertex_s}:
	r[v_s, v2_v] <= b[v1_v, v2_v, v_s];
subject to S11 {(v1_v, v2_v) in edge_v, v_s in vertex_s}:
	r[v_s, v1_v]+r[v_s, v2_v] >= b[v1_v, v2_v, v_s];
subject to S12 {(v1_v, v2_v) in edge_v, v1_s in vertex_s}:
	((sum {(v_s1,v_s2) in edge_s: v_s1 = v1_s or v_s2 = v1_s} l[v_s1, v_s2, v1_v,v2_v]) -1) + 2*N[v1_v, v2_v, v1_s] >= 1 - b[v1_v, v2_v, v1_s];
subject to S13 {(v1_v, v2_v) in edge_v, v1_s in vertex_s}:
	-((sum {(v_s1,v_s2) in edge_s: v_s1 = v1_s or v_s2 = v1_s} l[v_s1, v_s2, v1_v,v2_v]) -1) + 2*(1-N[v1_v, v2_v, v1_s]) >= 1 - b[v1_v, v2_v, v1_s];

#	sum {v2_s in vertex_s: (v1_s,v2_s) in edge_s} l[v1_s, v2_s, v1_v, v2_v] = 2 - b[v1_v, v2_v, v1_s];


##### Data
data;
## Virtual Graph
param : vertex_v : d_v :=
	0 88
	1 78
	2 94
	3 35
	4 74
	5 28
	6 92
	7 78
	8 50
	9 81;

param : edge_v : d_e :=
	0 8 4
	1 9 14
	1 6 44
	1 5 26
	2 5 26
	2 4 2
	3 6 25
	5 8 27
	6 7 16;


## Physical Graph
param : vertex_s : c_v :=
	0 14
	1 40
	2 96
	3 15
	4 33
	5 6
	6 9
	7 9
	8 12
	9 26
	10 46
	11 40
	12 32
	13 55
	14 92
	15 38
	16 62
	17 78
	18 38
	19 80
	20 86
	21 81
	22 63
	23 86
	24 12
	25 13
	26 65
	27 44
	28 19
	29 37
	30 98
	31 84
	32 71
	33 29
	34 82
	35 34
	36 7
	37 65
	38 26
	39 33
	40 56
	41 49
	42 86
	43 56
	44 4
	45 24
	46 43
	47 59
	48 49
	49 6;

param : edge_s : c_e :=
	0 26 81
	0 21 34
	0 20 79
	0 15 32
	0 11 72
	0 5 84
	1 45 30
	1 44 81
	1 31 56
	1 4 89
	2 46 55
	2 41 89
	2 37 2
	2 24 88
	2 13 49
	3 31 53
	3 21 39
	3 4 7
	4 48 2
	4 42 92
	4 39 83
	4 17 72
	4 11 47
	5 39 2
	5 29 62
	5 8 31
	6 39 77
	6 34 85
	6 25 48
	6 20 87
	7 48 10
	7 30 72
	8 46 92
	8 40 7
	8 26 27
	8 21 64
	8 17 79
	9 42 68
	9 13 55
	10 43 91
	10 30 47
	10 22 29
	10 21 92
	10 19 94
	11 36 12
	11 21 40
	11 15 12
	12 44 31
	12 42 96
	12 38 90
	12 37 26
	12 25 100
	13 31 67
	13 27 12
	14 47 63
	14 45 78
	14 28 23
	15 42 19
	15 38 94
	15 35 52
	15 26 93
	15 22 45
	15 18 40
	16 24 20
	16 17 53
	17 46 31
	17 45 62
	17 34 34
	17 29 17
	18 26 45
	19 44 26
	20 49 81
	21 44 70
	21 42 25
	21 37 13
	22 45 14
	22 33 100
	23 49 48
	23 40 100
	23 26 39
	24 34 45
	24 33 45
	24 32 36
	25 44 19
	25 36 89
	25 31 35
	25 29 36
	26 49 96
	26 41 27
	26 38 4
	27 36 87
	29 37 35
	29 30 22
	30 46 30
	31 34 2
	31 32 92
	32 46 98
	32 33 24
	33 37 86
	34 43 64
	35 39 32
	37 49 85
	38 40 76
	38 39 23
	39 47 51
	39 46 42
	40 47 36
	41 49 46
	41 45 85
	41 42 96
	42 43 26
	43 46 22;

end;
