# tiny-chess-bot: 4 KB chess engine, iterative-deepening alpha-beta with PVS, killer moves,
# quiescence, a tapered piece-square eval and a node budget counted in nodes
# (never in seconds), so every trial and its replay play the same moves.
import os,json,urllib.request


def T():
	global K,W,P,J,X,C,I
	K=[0]*128;W=[0]*128;P=([0]*128,[0]*128)
	for s in range(128):
		if s&136:continue
		for d in(33,31,18,14,-14,-18,-31,-33):
			t=s+d
			if not t&136:K[s]|=1<<t
		for d in(1,-1,16,-16,15,17,-15,-17):
			t=s+d
			if not t&136:W[s]|=1<<t
		for d in(-15,-17):
			t=s+d
			if not t&136:P[0][s]|=1<<t
		for d in(15,17):
			t=s+d
			if not t&136:P[1][s]|=1<<t
	j=[[0]*64 for _ in range(7)];x=[[0]*64 for _ in range(7)]
	a=(0,0,6,14,26,42,64,0);b=(0,0,8,16,28,46,72,0);k=(0,-10,-24,-40,-56,-72,-88,0)
	for r in range(8):
		for f in range(8):
			c=min(f,7-f)+min(r,7-r);i=r*8+f;w=10 if f in(3,4)else 5 if f in(2,5)else 0
			j[1][i]=a[r]+w;x[1][i]=b[r]+w+2
			j[2][i]=6*c-20;x[2][i]=4*c-10
			j[3][i]=4*c-8;x[3][i]=4*c-8
			j[4][i]=5*c-16+(14 if r==6 else 0);x[4][i]=4*c-10
			j[5][i]=4*c-14+(10 if r==6 else 0);x[5][i]=6*c-16
			j[6][i]=k[r]+(12 if r==0 and f in(2,6)else 0);x[6][i]=8*c-24
	J=[tuple(t)for t in j];X=[tuple(t)for t in x]
	C=[15]*128;C[4]=12;C[7]=14;C[0]=13;C[116]=3;C[119]=11;C[112]=7
	I=([0]*128,[0]*128)
	for s in range(128):I[0][s]=(s>>4)*8+(s&7);I[1][s]=(7-(s>>4))*8+(s&7)


class B:
	def __init__(A):
		A.c=[0]*128;A.a=[0]*16;A.k=[0,0];A.o=0;A.d=0;A.f=-1;A.i=[0,0]
		A.j=A.e=A.n=A.b=0;A.p=[];A.l=A.m=0;A.g=False;A.w=[[0,0]for _ in range(64)]

	def F(A,fen):
		V=A.c=[0]*128;R=A.a=[0]*16;A.k=[0,0];A.j=A.e=A.n=A.b=0;A.p=[];A.l=A.m=0;A.g=False
		w=fen.split();s=w[0].split('/')
		for r,row in enumerate(s):
			rank=7-r;f=0
			for ch in row:
				if ch.isdigit():f+=int(ch)
				else:
					t='pnbrqk'.index(ch.lower())+1;c=0 if ch.isupper()else 1;q=rank*16+f;pc=t|c<<3
					V[q]=pc;R[c*8+t]|=1<<q;A.k[c]|=1<<q;A.n+=(0,0,1,1,2,4,0)[t]
					if t==6:A.i[c]=q
					g=1 if c==0 else-1;d=I[c][q]
					A.j+=g*((0,100,320,330,500,900,0)[t]+J[t][d]);A.e+=g*((0,100,320,330,500,900,0)[t]+X[t][d]);f+=1
		A.o=0 if w[1]=='w'else 1;A.d=0;g=w[2]
		if'K'in g:A.d|=1
		if'Q'in g:A.d|=2
		if'k'in g:A.d|=4
		if'q'in g:A.d|=8
		A.f=-1
		if w[3]!='-':A.f=(int(w[3][1])-1)*16+(ord(w[3][0])-97)
		A.b=int(w[4])if len(w)>4 else 0

	def U(A,m):
		q=m&127;t=m>>7&127;r=m>>14&7
		return'abcdefgh'[q&7]+str((q>>4)+1)+'abcdefgh'[t&7]+str((t>>4)+1)+(' pnbrq'[r]if r else'')

	def H(A,s,by):
		if K[s]&A.a[by*8+2]or W[s]&A.a[by*8+6]or P[by][s]&A.a[by*8+1]:return True
		V=A.c
		for d in(-15,-17,15,17):
			t=s+d
			while not t&136:
				p=V[t]
				if p:
					if p>>3==by and(p&7==3 or p&7==5):return True
					break
				t+=d
		for d in(-16,-1,1,16):
			t=s+d
			while not t&136:
				p=V[t]
				if p:
					if p>>3==by and(p&7==4 or p&7==5):return True
					break
				t+=d
		return False

	def G(A,caps=False):
		c=A.o;t=1-c;V=A.c;pcs=A.k[c];out=[];ep=A.f
		while pcs:
			b=pcs&-pcs;pcs^=b;q=b.bit_length()-1;p=V[q]&7
			if p==1:
				fwd=16 if c==0 else-16;t2=q+fwd
				if not t2&136 and V[t2]==0:
					if((t2>=112)if c==0 else(t2<16)):
						for x in(5,4,3,2):out.append(q|t2<<7|x<<14)
					elif not caps:
						out.append(q|t2<<7);d2=t2+fwd
						if not d2&136 and V[d2]==0 and((q<32)if c==0 else(q>=96)):out.append(q|d2<<7|1<<17)
				for t2 in((q+15,q+17)if c==0 else(q-15,q-17)):
					if t2&136:continue
					z=V[t2]
					if z and z>>3==t:
						if((t2>=112)if c==0 else(t2<16)):
							for x in(5,4,3,2):out.append(q|t2<<7|x<<14)
						else:out.append(q|t2<<7)
					elif t2==ep:out.append(q|t2<<7|2<<17)
			elif p==2 or p==6:
				m=K[q]if p==2 else W[q]
				while m:
					b=m&-m;m^=b;t2=b.bit_length()-1;z=V[t2]
					if z:
						if z>>3==t:out.append(q|t2<<7)
					elif not caps:out.append(q|t2<<7)
				if p==6 and not caps:
					if c==0 and q==4:
						if A.d&1 and V[5]==0 and V[6]==0 and not A.H(4,t)and not A.H(5,t):out.append(4|6<<7|3<<17)
						if A.d&2 and V[3]==0 and V[2]==0 and V[1]==0 and not A.H(4,t)and not A.H(3,t):out.append(4|2<<7|3<<17)
					elif c==1 and q==116:
						if A.d&4 and V[117]==0 and V[118]==0 and not A.H(116,t)and not A.H(117,t):out.append(116|118<<7|3<<17)
						if A.d&8 and V[115]==0 and V[114]==0 and V[113]==0 and not A.H(116,t)and not A.H(115,t):out.append(116|114<<7|3<<17)
			else:
				ds=(-15,-17,15,17)if p==3 else(-16,-1,1,16)if p==4 else(-16,-1,1,16,-15,-17,15,17)
				for d in ds:
					t2=q+d
					while not t2&136:
						z=V[t2]
						if z==0:
							if not caps:out.append(q|t2<<7)
							t2+=d
						else:
							if z>>3==t:out.append(q|t2<<7)
							break
		return out

	def M(A,m):
		q=m&127;t=m>>7&127;pr=m>>14&7;fl=m>>17&3;c=A.o;o=1-c;g=1 if c==0 else-1
		V=A.c;R=A.a;Z=A.k;pc=V[q];p=pc&7;cap=V[t];cs=t
		if fl==2:cs=t-16 if c==0 else t+16;cap=V[cs]
		ep=A.f;A.p.append((m,cap,cs,A.d,ep,A.j,A.e,A.n,A.b));A.f=-1
		A.b=0 if(cap or p==1)else A.b+1
		R[c*8+p]^=1<<q;Z[c]^=1<<q;V[q]=0;d=I[c][q]
		A.j-=g*((0,100,320,330,500,900,0)[p]+J[p][d]);A.e-=g*((0,100,320,330,500,900,0)[p]+X[p][d]);A.n-=(0,0,1,1,2,4,0)[p]
		if cap:
			cp=cap&7;cc=cap>>3;cg=1 if cc==0 else-1;R[cc*8+cp]^=1<<cs;Z[cc]^=1<<cs;V[cs]=0;e=I[cc][cs]
			A.j-=cg*((0,100,320,330,500,900,0)[cp]+J[cp][e]);A.e-=cg*((0,100,320,330,500,900,0)[cp]+X[cp][e]);A.n-=(0,0,1,1,2,4,0)[cp]
		nw=(pr|c<<3)if pr else pc;n=nw&7;V[t]=nw;R[c*8+n]|=1<<t;Z[c]|=1<<t;d=I[c][t]
		A.j+=g*((0,100,320,330,500,900,0)[n]+J[n][d]);A.e+=g*((0,100,320,330,500,900,0)[n]+X[n][d]);A.n+=(0,0,1,1,2,4,0)[n]
		if p==6:A.i[c]=t
		if fl==3:
			if t==6:a1,a2=7,5
			elif t==2:a1,a2=0,3
			elif t==118:a1,a2=119,117
			else:a1,a2=112,115
			rk=4|c<<3;V[a1]=0;V[a2]=rk;R[c*8+4]^=(1<<a1)|(1<<a2);Z[c]^=(1<<a1)|(1<<a2)
			A.j+=g*(J[4][I[c][a2]]-J[4][I[c][a1]]);A.e+=g*(X[4][I[c][a2]]-X[4][I[c][a1]])
		A.d&=C[q]&C[t]
		if fl==1:A.f=(q+t)>>1
		A.o=o
		if A.H(A.i[c],o):A.N();return False
		return True

	def N(A):
		m,cap,cs,d,ep,j,e,n,hm=A.p.pop();q=m&127;t=m>>7&127;pr=m>>14&7;fl=m>>17&3;A.o^=1;c=A.o
		V=A.c;R=A.a;Z=A.k;pc=V[t];p=pc&7
		if pr:
			V[t]=0;R[c*8+p]^=1<<t;Z[c]^=1<<t;V[q]=1|c<<3;R[c*8+1]|=1<<q;Z[c]|=1<<q
		else:
			V[q]=pc;V[t]=0;R[c*8+p]^=(1<<t)|(1<<q);Z[c]^=(1<<t)|(1<<q)
		if p==6:A.i[c]=q
		if cap:
			cc=cap>>3;V[cs]=cap;R[cc*8+(cap&7)]|=1<<cs;Z[cc]|=1<<cs
		if fl==3:
			if t==6:a1,a2=7,5
			elif t==2:a1,a2=0,3
			elif t==118:a1,a2=119,117
			else:a1,a2=112,115
			V[a1]=4|c<<3;V[a2]=0;R[c*8+4]^=(1<<a1)|(1<<a2);Z[c]^=(1<<a1)|(1<<a2)
		A.d=d;A.f=ep;A.j=j;A.e=e;A.n=n;A.b=hm

	def V(A):
		n=A.n
		if n>24:n=24
		s=(A.j*n+A.e*(24-n))//24
		for c in(0,1):
			b=A.a[c*8+3]
			if b and b&(b-1):s+=22 if c==0 else-22
		return s if A.o==0 else-s

	def Q(A,alpha,beta,ply,qd):
		A.l+=1
		if A.m and A.l>=A.m:A.g=True;return 0
		if qd>=6 or ply>=40 or A.b>=100:return A.V()
		chk=A.H(A.i[A.o],1-A.o)
		if chk:best=-100000
		else:
			best=A.V()
			if best>=beta:return best
			if best>alpha:alpha=best
		V=A.c;s=[]
		for m in A.G(not chk):
			z=V[m>>7&127];v=(0,100,320,330,500,900,0)[z&7]*100-(V[m&127]&7)
			if m>>14&7:v+=900
			s.append((v,m))
		s.sort(key=lambda x:-x[0]);ok=0
		for v,m in s:
			if not A.M(m):continue
			ok+=1;z=-A.Q(-beta,-alpha,ply+1,qd+1);A.N()
			if A.g:return 0
			if z>best:
				best=z
				if z>alpha:
					alpha=z
					if alpha>=beta:break
		if chk and ok==0:return -100000+ply
		return best

	def S(A,depth,alpha,beta,ply):
		A.l+=1
		if A.m and A.l>=A.m:A.g=True;return 0
		if ply>=40 or A.b>=100:return A.V()
		chk=A.H(A.i[A.o],1-A.o)
		if chk:depth+=1
		if depth<1:return A.Q(alpha,beta,ply,0)
		V=A.c;c=A.o;s=[];km=A.w[ply]
		for m in A.G():
			q=m&127;t=m>>7&127;z=V[t];v=0
			if z:v=(0,100,320,330,500,900,0)[z&7]*1000000-(V[q]&7)
			elif m>>14&7:v=(m>>14&7)*100000
			if m==km[0]:v=80000000
			elif m==km[1]:v=70000000
			s.append((v,m))
		s.sort(key=lambda x:-x[0]);best=-1000000;bm=0;ok=0
		for v,m in s:
			if not A.M(m):continue
			ok+=1
			if ok==1:z=-A.S(depth-1,-beta,-alpha,ply+1)
			else:
				z=-A.S(depth-1,-alpha-1,-alpha,ply+1)
				if not A.g and alpha<z<beta:z=-A.S(depth-1,-beta,-alpha,ply+1)
			A.N()
			if A.g:return 0
			if z>best:
				best=z;bm=m
				if z>alpha:
					alpha=z
					if alpha>=beta:
						if m!=km[0]:km[1]=km[0];km[0]=m
						break
		if ok==0:return -100000+ply if chk else 0
		return best

	def R(A,cap):
		A.l=0;A.m=cap;A.g=False
		ok=[]
		for m in A.G():
			if A.M(m):A.N();ok.append(m)
		if not ok:return 0
		best=ok[0];o=ok
		for d in range(1,40):
			alpha=-1000000;res=[]
			for i,m in enumerate(o):
				if not A.M(m):continue
				if i==0:z=-A.S(d-1,-1000000,-alpha,1)
				else:
					z=-A.S(d-1,-alpha-1,-alpha,1)
					if not A.g and z>alpha:z=-A.S(d-1,-1000000,-alpha,1)
				A.N()
				if A.g:break
				res.append((z,m))
				if z>alpha:alpha=z
			if A.g or not res:break
			res.sort(key=lambda x:-x[0]);o=[m for z,m in res];best=o[0]
			if res[0][0]>=99900:break
		return best


def O():
	u=os.environ['MAKEFUN_ENV_URL'];hd={'content-type':'application/json'}
	def P(p,b):return json.load(urllib.request.urlopen(urllib.request.Request(u+p,json.dumps(b).encode(),hd),timeout=60))
	e=B();used=0;made=0
	while 1:
		g=P('/game',{})
		if g['status']=='done':break
		while g['status']=='your_move':
			legal=g['legal_moves'];e.F(g['fen']);c=(made+1)*AVG-used
			if c<MINCAP:c=MINCAP
			elif c>MAXCAP:c=MAXCAP
			if used>TOTAL:c=MINCAP
			m=0
			try:m=e.R(c)
			except Exception:m=0
			used+=e.l;made+=1
			t=e.U(m)if m else legal[0]
			if t not in legal:t=legal[0]
			try:g=P('/move',{'game':g['game'],'move':t})
			except Exception:g=P('/game',{})
			if g.get('status')=='done':break
		if g.get('status')=='done':break


T();AVG=80000;MAXCAP=130000;MINCAP=4000;TOTAL=28000000;O()
