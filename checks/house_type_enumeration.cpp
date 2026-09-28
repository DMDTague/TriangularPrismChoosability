// Complete type-count verification of the House Lemma for fixed k.
//
// House: base lists A1,A3 have size k-1; shoulder lists L2,L4 have size k;
// the roof list R has size k-1.  Colours in L2 union L4 are classified by
// (inL2,inL4,inR,inA1,inA3); colours outside L2 union L4 enter only through
// iOut = |A1 intersect A3 \ (L2 union L4)|.  Every configuration of five lists
// of these sizes is represented by one of the enumerated type configurations.
//
// The program checks
//   h >= target - sigma_k,
// and that h < target occurs only for the extremal Delta family.
#include <bits/stdc++.h>
using namespace std; typedef long long ll;
int k; ll tgt,smax;
struct Ty{int l2,l4,r,a1,a3;};
vector<Ty> TY;
ll S_of(const vector<int>&n,int iOut){
 ll I=iOut; for(size_t t=0;t<TY.size();t++) if(TY[t].a1&&TY[t].a3) I+=n[t];
 ll s=0;
 for(size_t t=0;t<TY.size();t++){ if(!n[t]||!TY[t].l2) continue;
  for(size_t u=0;u<TY.size();u++){ if(!n[u]||!TY[u].l4) continue;
   ll pairs=(ll)n[t]*(n[u]-(t==u?1:0)); if(pairs<=0) continue;
   ll w=k-1-TY[t].r-TY[u].r;
   ll g=(ll)(k-1-TY[t].a1)*(k-1-TY[u].a3)-I+(TY[t].a1&TY[t].a3)+(TY[u].a1&TY[u].a3);
   s+=pairs*w*g;}}
 return s;}
ll brute(const vector<int>&A1,const vector<int>&A3,const vector<int>&L2,const vector<int>&L4,const vector<int>&R){ll n=0;
 for(int c1:A1)for(int c3:A3)if(c1!=c3)for(int c2:L2)if(c2!=c1)for(int c4:L4)if(c4!=c2&&c4!=c3)for(int c5:R)if(c5!=c2&&c5!=c4)n++;return n;}
void comps(int total,int parts,vector<int>&cur,vector<vector<int>>&out){ if(parts==1){cur.push_back(total);out.push_back(cur);cur.pop_back();return;}
 for(int i=0;i<=total;i++){cur.push_back(i);comps(total-i,parts-1,cur,out);cur.pop_back();}}
int main(int argc,char**argv){
 if(argc!=2){cerr << "usage: " << argv[0] << " k\n"; return 2;}
 k=atoi(argv[1]); if(k<4){cerr << "k must be >= 4\n"; return 2;}
 ll o=(ll)(k-2)*(k*k*k-6*k*k+14*k-13); tgt=(ll)(k-1)*o; smax=2LL*(k-2)*(k-3);
 int blocks[3][2]={{1,1},{1,0},{0,1}};
 for(auto&b:blocks)for(int r=0;r<2;r++)for(int a1=0;a1<2;a1++)for(int a3=0;a3<2;a3++)TY.push_back({b[0],b[1],r,a1,a3});
 mt19937 rng(7); for(int tr=0;tr<400;tr++){int U=k+5;vector<int>pal(U);iota(pal.begin(),pal.end(),0);
  auto samp=[&](int m){shuffle(pal.begin(),pal.end(),rng);return vector<int>(pal.begin(),pal.begin()+m);};
  auto A1=samp(k-1),A3=samp(k-1),L2=samp(k),L4=samp(k),R=samp(k-1);
  vector<int>n(24,0);set<int>U24(L2.begin(),L2.end());U24.insert(L4.begin(),L4.end());
  auto in=[&](const vector<int>&v,int c){return (int)count(v.begin(),v.end(),c);};
  for(int c:U24){int l2=in(L2,c),l4=in(L4,c),r=in(R,c),a1=in(A1,c),a3=in(A3,c);for(int t=0;t<24;t++)if(TY[t].l2==l2&&TY[t].l4==l4&&TY[t].r==r&&TY[t].a1==a1&&TY[t].a3==a3)n[t]++;}
  int iOut=0;for(int c:A1)if(in(A3,c)&&!U24.count(c))iOut++;
  if(S_of(n,iOut)!=brute(A1,A3,L2,L4,R)){printf("VALIDATION FAIL\n");return 1;}}
 printf("k=%d: formula validated vs brute force on 400 random configs\n",k);
 ll nconf=0,minAll=LLONG_MAX,defic=0,deficBad=0,minNonFam=LLONG_MAX;
 for(int a=0;a<=k;a++){
  vector<vector<int>>C11,C10,C01;vector<int>cur;comps(a,8,cur,C11);comps(k-a,8,cur,C10);comps(k-a,8,cur,C01);
  for(auto&x:C11)for(auto&y:C10)for(auto&z:C01){
   vector<int>n(24);for(int i=0;i<8;i++){n[i]=x[i];n[8+i]=y[i];n[16+i]=z[i];}
   int rV=0,a1V=0,a3V=0;for(int t=0;t<24;t++){rV+=TY[t].r*n[t];a1V+=TY[t].a1*n[t];a3V+=TY[t].a3*n[t];}
   if(rV>k-1||a1V>k-1||a3V>k-1)continue;
   int o1=k-1-a1V,o3=k-1-a3V;
   for(int iOut=0;iOut<=min(o1,o3);iOut++){
    ll s=S_of(n,iOut)-tgt; nconf++; minAll=min(minAll,s);
    bool fam=(a==k)&&iOut==0;
    if(fam){
     for(int t=0;t<24;t++){int want=0;const Ty&T=TY[t];
      if(T.l2&&T.l4&&T.r&&T.a1&&T.a3)want=k-2;
      else if(T.l2&&T.l4&&!T.r&&T.a1&&T.a3)want=1;
      else if(T.l2&&T.l4&&T.r&&!T.a1&&!T.a3)want=1;
      if(n[t]!=want){fam=false;break;}}}
    if(s<0){defic++; if(!fam)deficBad++;}
    if(!fam)minNonFam=min(minNonFam,s);
   }}}
 printf("k=%d: type-configs=%lld  min(S-target)=%lld (=-smax=%lld? %s)  deficient=%lld  deficient outside family=%lld  min(S-target) outside family=%lld\n",
  k,nconf,minAll,-smax,minAll==-smax?"yes":"NO",defic,deficBad,minNonFam);
 return deficBad?1:0;}
