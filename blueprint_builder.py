#!/usr/bin/env python3
"""CC0. Rebuild the Rev B drawing expansion. No measured geometry is implied."""
from pathlib import Path
import math, json, hashlib, zipfile
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parent
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf')
if not FONT_DIR.exists():
    import matplotlib
    FONT_DIR = Path(matplotlib.get_data_path()) / 'fonts' / 'ttf'
for name, fn in [('Sans','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT_DIR/fn)))

W,H = 1224,792
NAVY=HexColor('#163751'); BLUE=HexColor('#356A8A'); PALE=HexColor('#F3F8FB')
GRID=HexColor('#DCE8EF'); GRAY=HexColor('#536773'); TEAL=HexColor('#176D6B')
AMBER=HexColor('#946014'); RED=HexColor('#A13F3B'); LIGHT=HexColor('#FFF5E6')
PDF=OUT/'Five_String_Acoustic_Resonator_Rev_B_Blueprints_17_Sheets.pdf'
c=canvas.Canvas(str(PDF),pagesize=(W,H),pageCompression=1)
c.setTitle('Five-String Acoustic Resonator - Rev B - 17-Sheet Blueprint Expansion')
c.setAuthor('Anonymous')
c.setSubject('Provisional engineering coordination drawings. Not a cutting drawing. CC0 1.0.')
checks=[]
SHEETS=[
('G00','Drawing set and general notes'),('G01','Source record and corrections'),
('A01','General arrangement: elevations'),('A02','Plan sections and vessel clearance'),
('A03','Exploded assembly and parts register'),('D01','Base, feet and support geometry'),
('D02','Spine section and force system'),('D03','Upper anchor and tuner interface'),
('D04','Lower anchor and frame closure'),('D05','Anchor bar pattern and bending axes'),
('D06','Vessel support and removable top'),('M01','Candidate string schedule'),
('M02','Load cases and calculation record'),('M03','Stability and restraint geometry'),
('Q01','Field measurement sheets'),('Q02','Assembly and inspection sequence'),
('Q03','Acoustic measurement and release record')]

def line(x1,y1,x2,y2,color=NAVY,width=1,dash=None):
    c.setStrokeColor(color);c.setLineWidth(width);c.setDash(dash or [])
    c.line(x1,y1,x2,y2);c.setDash([])
def rect(x,y,w,h,stroke=GRID,fill=None,width=.8,dash=None):
    c.setStrokeColor(stroke);c.setLineWidth(width);c.setDash(dash or [])
    if fill:c.setFillColor(fill)
    c.rect(x,y,w,h,stroke=1,fill=bool(fill));c.setDash([])
def ellipse(x,y,w,h,color=BLUE,fill=None,width=1.3,dash=None):
    c.setStrokeColor(color);c.setLineWidth(width);c.setDash(dash or [])
    if fill:c.setFillColor(fill)
    c.ellipse(x,y,x+w,y+h,stroke=1,fill=bool(fill));c.setDash([])
def circle(x,y,r,color=BLUE,fill=None,width=1):
    ellipse(x-r,y-r,r*2,r*2,color,fill,width)
def text(x,y,s,size=10,font='Sans',color=NAVY,align='left'):
    s=str(s); c.setFillColor(color);c.setFont(font,size)
    sw=pdfmetrics.stringWidth(s,font,size)
    if align=='center':c.drawCentredString(x,y,s);xx=x-sw/2
    elif align=='right':c.drawRightString(x,y,s);xx=x-sw
    else:c.drawString(x,y,s);xx=x
    checks.append((page_no,xx,y,xx+sw,y+size,s))
def para(x,top,w,s,size=10.5,color=NAVY,font='Sans',leading=None):
    leading=leading or size*1.42
    for p in s.split('\n'):
        for t in simpleSplit(p,font,size,w):
            text(x,top-size,t,size,font,color);top-=leading
        if not p:top-=leading*.55
    return top
def note(x,top,w,title,body,color=BLUE):
    text(x,top,title,11,'Bold',color)
    return para(x,top-11,w,body,10.4)-13
def tag(x,y,s,color=AMBER):
    ww=pdfmetrics.stringWidth(s,'Bold',8.5)+14
    rect(x,y-4,ww,17,stroke=color,fill=white)
    text(x+7,y+1,s,8.5,'Bold',color)
def arrow(x1,y1,x2,y2,color=RED,width=1.4,head=6):
    line(x1,y1,x2,y2,color,width)
    a=math.atan2(y2-y1,x2-x1)
    p=c.beginPath();p.moveTo(x2,y2)
    p.lineTo(x2-head*math.cos(a-.42),y2-head*math.sin(a-.42))
    p.lineTo(x2-head*math.cos(a+.42),y2-head*math.sin(a+.42));p.close()
    c.setFillColor(color);c.drawPath(p,fill=1,stroke=0)
def dimh(x1,x2,y,ref1,ref2,label,color=AMBER):
    line(x1,ref1,x1,y+4,color,.6);line(x2,ref2,x2,y+4,color,.6)
    arrow(x1,y,x2,y,color,.7,5);arrow(x2,y,x1,y,color,.7,5)
    ww=pdfmetrics.stringWidth(label,'Mono',9)+10
    c.setFillColor(white);c.rect((x1+x2-ww)/2,y+3,ww,14,fill=1,stroke=0)
    text((x1+x2)/2,y+6,label,9,'Mono',color,'center')
def dimv(y1,y2,x,ref1,ref2,label,color=AMBER):
    line(ref1,y1,x+3,y1,color,.6);line(ref2,y2,x+3,y2,color,.6)
    arrow(x,y1,x,y2,color,.7,5);arrow(x,y2,x,y1,color,.7,5)
    c.saveState();c.translate(x-5,(y1+y2)/2);c.rotate(90)
    c.setFillColor(white);ww=pdfmetrics.stringWidth(label,'Mono',9)+10
    c.rect(-ww/2,-3,ww,14,fill=1,stroke=0)
    c.setFillColor(color);c.setFont('Mono',9);c.drawCentredString(0,0,label);c.restoreState()
def leader(points,label,tx,ty,w=160,color=BLUE):
    for (x1,y1),(x2,y2) in zip(points,points[1:]):line(x1,y1,x2,y2,color,.8)
    circle(*points[0],2,color,color)
    para(tx,ty,w,label,9.5,color)
def panel(x,y,w,h,title,grid=False):
    rect(x,y,w,h,fill=PALE)
    if grid:
        for xx in range(int(x+18),int(x+w),18):line(xx,y,xx,y+h-31,GRID,.25)
        for yy in range(int(y+18),int(y+h-31),18):line(x,yy,x+w,yy,GRID,.25)
    text(x+13,y+h-21,title,11,'Bold',BLUE)
    line(x,y+h-31,x+w,y+h-31,GRID,.7)
def table(x,top,widths,headers,rows,size=9.5,minh=29):
    total=sum(widths);hh=29
    rect(x,top-hh,total,hh,stroke=NAVY,fill=NAVY)
    xx=x
    for w,s in zip(widths,headers):
        para(xx+8,top-6,w-16,s,9,white,font='Bold',leading=11)
        xx+=w
    y=top-hh
    for ri,row in enumerate(rows):
        n=max(sum(max(1,len(simpleSplit(p,'Sans',size,w-16))) for p in str(s).split('\n')) for s,w in zip(row,widths))
        rh=max(minh,n*size*1.35+14)
        rect(x,y-rh,total,rh,fill=(PALE if ri%2==0 else white))
        xx=x
        for w,s in zip(widths,row):
            para(xx+8,y-6,w-16,str(s),size,leading=size*1.35)
            if xx>x:line(xx,y-rh,xx,y,GRID,.6)
            xx+=w
        y-=rh
    return y
def formula(x,y,s,size=12):text(x,y,s,size,'Mono',NAVY)
def page(idx,kicker='ENGINEERING COORDINATION / PROVISIONAL'):
    global page_no
    page_no=idx; code,title=SHEETS[idx-1]
    c.bookmarkPage(code);c.addOutlineEntry(code+' - '+title,code,level=0)
    rect(24,24,1176,744,stroke=NAVY,width=1.2)
    text(42,744,'FIVE-STRING ACOUSTIC RESONATOR',12,'Bold')
    text(1182,744,'REV B  /  DRAWING EXPANSION 01',10,'Mono',BLUE,'right')
    text(42,710,title.upper(),24,'Bold')
    text(42,689,kicker,9,'Mono',GRAY)
    line(24,677,1200,677,NAVY,1)
    line(24,90,1200,90,NAVY,1)
    text(40,71,'PUBLIC DOMAIN - CC0 1.0  |  AUTHOR: ANONYMOUS',8.5,'Bold')
    text(40,54,'PROVISIONAL - NOT A CUTTING DRAWING',11,'Bold',RED)
    text(40,37,'Actual dimensions, string data and load-path review required before fabrication or tensioning.',8.4,color=GRAY)
    line(688,24,688,90,NAVY,.7);line(985,24,985,90,NAVY,.7)
    text(704,70,'ISSUE 2026-09-08  |  ANSI B 17 x 11 in',8.5,'Mono')
    text(704,53,'UNITS: in [mm] unless stated',8.7)
    text(704,37,'NTS - DO NOT SCALE DRAWINGS',9,'Bold',BLUE)
    text(1003,58,'FSR-B-'+code,22,'Bold')
    text(1003,36,f'SHEET {idx:02d} / 17  |  REVIEW / MEASURE',8.5,'Mono',GRAY)
def end():c.showPage()
def vessel(cx,y,h,w=145):
    p=c.beginPath();p.moveTo(cx-w*.3,y)
    p.curveTo(cx-w*.75,y+h*.25,cx-w*.65,y+h*.62,cx-w*.27,y+h)
    p.lineTo(cx+w*.27,y+h)
    p.curveTo(cx+w*.65,y+h*.62,cx+w*.75,y+h*.25,cx+w*.3,y)
    p.close();c.setStrokeColor(BLUE);c.setLineWidth(1.5);c.setDash([5,3]);c.drawPath(p);c.setDash([])
    ellipse(cx-w*.45,y+h*.49,w*.9,13,GRID,width=.7)
def front(cx,y,s=1,details=True):
    # Presentation coordinates only; no unmarked manufacturing dimensions.
    line(cx,y-18,cx,y+440*s,BLUE,.6,[8,3,2,3])
    rect(cx-90*s,y,180*s,16*s,NAVY,white,1.4)
    for dx in [-68,68]:rect(cx+(dx-8)*s,y-10*s,16*s,10*s,NAVY,white)
    rect(cx-11*s,y+16*s,22*s,386*s,AMBER,Color(.98,.95,.86),1.4)
    vessel(cx,y+55*s,298*s,128*s)
    for yy in [y+42*s,y+364*s]:rect(cx-66*s,yy,132*s,15*s,NAVY,white,1.4)
    for dx in [-40,-20,0,20,40]:
        line(cx+dx*s,y+56*s,cx+dx*s,y+364*s,NAVY,.85)
        for yy in [y+50*s,y+371*s]:circle(cx+dx*s,yy,2.4*s,NAVY,white)
    ellipse(cx-90*s,y+402*s,180*s,12*s,NAVY,white)
    for yy in [y+115*s,y+282*s]:
        rect(cx-83*s,yy,13*s,21*s,TEAL,white)
        rect(cx+70*s,yy,13*s,21*s,TEAL,white)
    if details:
        tag(cx-76*s,y+427*s,'5 STRINGS / SINGLE PLANE',BLUE)

# 01 - cover
page(1,'PASSIVE ACOUSTIC PROTOTYPE / MEASUREMENT PLATFORM')
panel(42,111,425,548,'01  /  ASSEMBLY REFERENCE',True)
front(254,164,1)
text(254,123,'Shell outline is symbolic; actual profile is unmeasured.',9,color=GRAY,align='center')
text(491,637,'17 sheets. One traceable Rev B set.',22,'Bold')
para(491,618,685,'Elevations, sections, part interfaces, force diagrams, candidate string calculations, and field records. This issue expands the drawing detail and corrects the supplied PDF calculations; it records no fabricated or tested assembly.',11)
tag(491,550,'N  NOMINAL / FROM REV B',AMBER);tag(717,550,'C  CALCULATED / CONDITIONAL',TEAL);tag(982,550,'U  UNRESOLVED',RED)
left=SHEETS[1:9];right=SHEETS[9:]
for xx,items in [(491,left),(846,right)]:
    yy=513
    for code,title in items:
        text(xx,yy,code,10,'Mono',TEAL)
        para(xx+46,yy+10,286,title,10.2)
        yy-=33
line(491,225,1182,225,GRID,1)
y=note(491,203,685,'DRAWING RULE','All dimensions retain their status. N values are planning dimensions, C values depend on written assumptions, and U values require measurement, selection or calculation. Blank fields mean unresolved.',BLUE)
note(491,y,685,'ISSUE STATUS','The primary string load path is the frame and its joints. The vessel has independent padded support. No certified capacity, final hole schedule, deflection result or acoustic performance is established by this set.',RED)
end()

# Remaining sheet functions are defined below and called after sheets 1-8.

# 02 - sources and corrections
page(2,'SOURCE LINEAGE / CORRECTIONS APPLIED TO THIS DRAWING EXPANSION')
text(42,649,'SOURCE REGISTER',12,'Bold',BLUE)
source_rows=[
('S1','Rev B Schematic Update (DOCX), dated 5 Sep 2026','Nominal geometry, parts P1-P15, independent vessel support and release conditions.'),
('S2','String tension gate PDF, 15 pages','Worked examples and CX-1 proposals. Recomputed; no part rating accepted from narrative.'),
('S3','Updated schematic PNG, two attached copies','Byte-identical reference drawing. One source, not two confirmations.'),
('S4','1000012794.png + GitHub screenshot','Appearance reference only. Collar shapes and depicted hardware are not fabrication evidence.'),
('S5','Five_String_Acoustic_Resonator_Rev_B.md','Conversation transcript despite filename. Not the original design specification.')]
table(42,635,[38,250,260],['ID','SUPPLIED SOURCE','USE IN THIS ISSUE'],source_rows,9.4,34)
text(615,649,'CALCULATION CORRECTIONS / S2',12,'Bold',BLUE)
corrections=[
('p5','G3 is 195.9977 Hz at A4 = 440 Hz equal temperament. 195.00 was a label error. Recomputed total: 70.84 lbf.'),
('p7','Rectangular kern: S/A = d/6, not d/2. Moving the string-plane force to the face still requires its equivalent couple.'),
('p8-10','Attachment span is not automatically speaking length. Clear-wood averages and Euler examples do not rate an ungraded member or identify the first failure.'),
('p11','A couple uses perpendicular reaction separation. The collar estimate H = Pe/d lacks a resolved reaction geometry.'),
('p12','For the stated two-string cantilever at a 1.5 in-wide support, M is about 69.09 lbf-in on the left, not 113.'),
('p12-15','No universal 11 in bar minimum or 2D rule is adopted. A 1.5 in-high bar cannot contain bolt centers 1.5 in apart with positive top/bottom margins.'),
('p13-15','Bolt gauge runs along z, not across the 2.5 in section depth. M/g is a couple force, not a complete per-bolt prying check.')]
table(615,635,[54,513],['PAGE','CORRECTION / CONSEQUENCE'],corrections,9.5,35)
text(42,305,'REFERENCE SOURCES CHECKED 8 SEP 2026',11,'Bold',BLUE)
urls=[
('W1  UNSW - ideal string relation','https://www.phys.unsw.edu.au/jw/strings.html'),
('W2  Baker & Haynes - static equivalence','https://eng.libretexts.org/Bookshelves/Mechanical_Engineering/Engineering_Statics:_Open_and_Interactive_(Baker_and_Haynes)/04:_Moments_and_Static_Equivalence/4.07:_Statically_Equivalent_Systems'),
('W3  USDA Forest Products Laboratory - Wood Handbook','https://research.fs.usda.gov/treesearch/62200'),
('W4  D\'Addario - current string tension calculator','https://www.daddario.com/pages/string-tension-pro-string-tension-calculator')]
yy=282
for label,url in urls:
    text(42,yy,label,10,color=TEAL);c.linkURL(url,(42,yy-3,588,yy+11),relative=0);yy-=24
para(42,yy,546,'W4: the historical chart URL redirected to the current calculator. The attached unit weights are transcribed inputs, not independently reconfirmed product data. The source archive records filenames and SHA-256 hashes.',9.7)
para(615,174,567,'Audit additions on A02 and D05 are conditional geometry checks. This set does not select CX-1 as an approved connection. The original source files remain the historical record.',10.5,color=RED)
end()

# 03 - elevations
page(3,'ALIGNED ORTHOGRAPHIC VIEWS / ALL OUTLINES NTS')
panel(42,113,396,546,'01  /  FRONT ELEVATION',True)
panel(451,113,386,546,'02  /  SIDE ELEVATION (+y TO RIGHT)',True)
panel(850,113,332,546,'DATUM / DIMENSION REGISTER')
front(244,168,.94,False)
dimv(158,557,88,159,159,'H = 42 [1067] N')
dimv(221,510,378,282,282,'L = 32 [812.8] N')
dimh(159,329,143,168,168,'BASE OD 16 [406.4] N')
tag(161,582,'SHELL SHAPE U',BLUE)
# Side elevation: centered spine, strings forward.
cx=579;y=168
rect(500,y,218,16,NAVY,white,1.4)
rect(cx-15,184,30,363,AMBER,Color(.98,.95,.86),1.4)
vessel(615,220,272,110)
for yy in [208,510]:
    rect(680,yy,18,14,NAVY,white)
    rect(cx-24,yy-9,57,33,RED,None,1,[4,3])
    line(cx+33,yy+7,680,yy+7,RED,1.2,[4,3])
line(689,222,689,510,NAVY,1.5)
line(cx,151,cx,582,BLUE,.6,[8,3,2,3])
ellipse(500,557,218,10,NAVY,white)
for xx in [524,690]:rect(xx,158,18,10,NAVY,white)
dimh(594,689,434,411,411,'c = 2-3 in N')
dimh(cx,689,389,370,370,'e = d/2 + c  C')
leader([(603,525),(727,539)],'Joint zone U\nSee D03 / D04',717,580,105,RED)
text(469,125,'Vessel supports omitted in side view for clarity.',8.5,color=GRAY)
y=table(863,615,[73,231],['ITEM','VALUE / STATUS'],[
('A','Base upper face: field datum z = 0.'),('B','Spine centroid axis: x = y = 0.'),
('x','Across the five-string array.'),('y','From spine axis toward strings.'),('z','Vertical, positive upward.'),
('L','32 in N; planning 28-36. Bearing-to-bearing; five lengths within 1/16 in unless scaled.'),('H','42 in N; planning 36-48. Overall datum chain U.'),
('d, b','Actual spine depth and width U.'),('c','Face-to-string-plane gap; min 1.5 in in S1.')],9.5,29)
para(863,y-15,304,'Vertical closure is unresolved: nominal 40 in spine, base thickness, feet, top mount and overlaps must be reconciled with nominal 42 in overall height. Do not derive cutting lengths from this elevation.',9.8,color=RED)
end()

# 04 - plan and clearance
page(4,'FIT THE COMPLETE HARDWARE ENVELOPE AT EVERY OCCUPIED HEIGHT z')
panel(42,296,552,363,'01  /  TRANSVERSE SECTION THROUGH STRINGS',True)
panel(611,296,571,363,'02  /  CONDITIONAL CX-1 BAR ENVELOPE',True)
cx,cy,sc=308,464,18
circle(cx,cy,7.0208*sc,BLUE,None,1.7)
rect(cx-1*sc,cy-1.5*sc,2*sc,3*sc,AMBER,Color(.98,.95,.86))
line(cx-145,cy,cx+145,cy,BLUE,.6,[8,3,2,3]);line(cx,cy-145,cx,cy+145,BLUE,.6,[8,3,2,3])
for x in [-4,-2,0,2,4]:circle(cx+x*sc,cy+4.5*sc,3.2,NAVY,NAVY)
line(cx-4*sc,cy+4.5*sc,cx+4*sc,cy+4.5*sc,NAVY,1)
arrow(cx,cy,cx+4*sc,cy+4.5*sc,TEAL,1)
dimh(cx-4*sc,cx+4*sc,590,cy+4.5*sc,cy+4.5*sc,'4s = 8 in N')
text(83,317,'Example: d = 3, c = 3, s = 2, radial allowance = 1 in.',9.5)
text(cx-20,cy-12,'B',10,'Bold',TEAL)
cx,cy,sc=895,467,16
circle(cx,cy,8.65261*sc,BLUE,None,1.7)
circle(cx,cy,7.0208*sc,GRID,None,.9)
rect(cx-sc,cy-1.5*sc,2*sc,3*sc,AMBER,Color(.98,.95,.86))
rect(cx-6*sc,cy+4.25*sc,12*sc,.5*sc,RED,white,1.6)
for xx in [-4,-2,0,2,4]:circle(cx+xx*sc,cy+4.5*sc,2.8,NAVY,NAVY)
arrow(cx,cy,cx+6*sc,cy+4.75*sc,TEAL,1)
dimh(cx-6*sc,cx+6*sc,588,539,539,'12 in BAR CANDIDATE / U')
text(639,317,'Bar thickness assumed 0.5 in along y; no tuners or bolt heads.',9.5)
formula(42,266,'D_clear(z) >= 2 [ sqrt(x_max^2 + y_max^2) + allowance(z) ]',12)
para(42,250,553,'Centered circular section only. For the strings alone: 2[sqrt(4^2 + 4.5^2) + 1] = 14.04 in. This is a conditional screen, not a measured vessel diameter.',10.4)
para(611,250,571,'For the illustrated 12 in bar: 2[sqrt(6^2 + 4.75^2) + 1] = 17.31 in before additional hardware. A 14.04 in string-only envelope cannot prove that this bar fits.',10.4,color=RED)
para(42,172,553,'General case: measure the actual inner boundary at each z and check all hardware corners, string excursion, tool access and installation path. A mouth smaller than the assembly can prevent insertion even if the belly fits.',10.4)
para(611,172,571,'Required decision: keep anchors outside the vessel, revise the hardware envelope, change the vessel, or revise the overall geometry with review. Anchor elevations relative to the mouth remain U.',10.4)
end()

# 05 - exploded assembly
page(5,'PART IDENTITIES FOLLOW S1 / EXPLODED SPACING DOES NOT SPECIFY ASSEMBLY HEIGHTS')
panel(42,112,454,547,'01  /  ASSEMBLY LAYERS',True)
cx=253
line(cx,137,cx,617,BLUE,.8,[8,3,2,3])
ellipse(cx-100,584,200,20,NAVY,white)
leader([(353,594),(392,602)],'P8  top',396,611,77)
rect(cx-67,526,134,19,NAVY,white)
leader([(320,536),(391,536)],'P3 / P4\nupper joint',395,550,80)
vessel(cx,285,206,129)
rect(cx-12,270,24,226,AMBER,Color(.98,.95,.86))
for xx in [-40,-20,0,20,40]:line(cx+xx,292,cx+xx,483,NAVY,.8)
leader([(339,408),(391,424)],'P7 shell\nP10 pads',395,438,79)
leader([(241,346),(115,343)],'P2 spine\nP5 strings',62,370,100)
rect(cx-67,237,134,19,NAVY,white)
leader([(320,248),(391,257)],'P3 / P6\nlower joint',395,270,79)
ellipse(cx-101,176,202,21,NAVY,white)
line(cx-101,186,cx-101,174,NAVY);line(cx+101,186,cx+101,174,NAVY)
ellipse(cx-101,164,202,21,NAVY)
for xx in [-74,0,74]:ellipse(cx+xx-10,131,20,12,TEAL,white)
text(65,126,'P1 base / P9 feet (four; three visible)',9.4)
parts=[('P1','Base','1','Two 3/4 in laminations; 16 in OD N. D01.'),('P2','Spine','1','Hard maple/ash; nominal 2 x 3 x 40 in. Actual U.'),('P3','Anchor bars','2','All section, holes and connections subject to review.'),('P4','Tuners','5','Exact product and mounting drawing U. D03.'),('P5','Strings','5','Candidate calculation M01; selected set U.'),('P6','Nut / bridge','2','Replaceable rounded bearing strips; shape U.'),('P7','Vessel','1','Material, profile, mass, wall and mouth U; measure per D06.'),('P8','Top plate','1','Thin metal or 1/4-3/8 in plywood; 14-18 in OD; mount U.'),('P9','Feet','4','Neoprene/Sorbothane, 1-1.5 in OD N; equal height; through-bolted.'),('P10','Padded supports','3-4','Straps/cleats independent of the string force loop.'),('P11','Restraint','1','Geometry and capacity determined separately. M03.'),('P12','Guards','As needed','Polycarbonate, anchor/tuner access and clearance U.'),('P13','Fasteners','Set','Grade-marked bolts, washers, locking nuts; size U. No wood screws in primary tension path.'),('P14','Passive pickup','Optional','Isolated, removable; mounting recorded. Q03.'),('P15','Powered exciter','Phase 2','Excluded from passive baseline. S1 constraints apply.')]
table(515,653,[42,128,62,435],['ID','PART','QTY','SPECIFICATION / STATUS'],parts,9.2,29)
end()

# 06 - base and support plan
page(6,'BASE DIMENSIONS N / FASTENER SIZES AND HOLE LOCATIONS U')
panel(42,272,558,387,'01  /  BASE PLAN',True)
cx,cy,sc=324,462,20
circle(cx,cy,8*sc,NAVY,white,1.6);circle(cx,cy,6.75*sc,BLUE,None,.8)
a=6.75*sc/math.sqrt(2)
rect(cx-a,cy-a,2*a,2*a,TEAL,None,1.6)
for dx in [-a,a]:
    for dy in [-a,a]:circle(cx+dx,cy+dy,11,TEAL,white,1.5)
rect(cx-20,cy-30,40,60,AMBER,Color(.98,.95,.86))
line(cx-180,cy,cx+180,cy,BLUE,.6,[8,3,2,3]);line(cx,cy-169,cx,cy+171,BLUE,.6,[8,3,2,3])
text(cx,cy-15,'B',10,'Bold',TEAL,'center')
dimh(cx-160,cx+160,285,cy,cy,'16 [406.4] OD N / MIN 14 in')
leader([(cx+a,cy+a),(525,596)],'4 feet on 13-14 in\ncenter circle N',448,630,142)
panel(617,425,565,234,'02  /  BASE EDGE SECTION')
rect(684,521,366,19,NAVY,white);rect(684,502,366,19,NAVY,white)
for xx in [720,996]:
    rect(xx,476,31,26,TEAL,white)
    line(xx+15.5,481,xx+15.5,549,RED,1,[4,3])
text(686,566,'Two nominal 3/4 in Baltic-birch layers (P1)',11)
dimv(502,540,1101,1050,1050,'1.5 [38.1] N')
para(638,464,522,'Bond specification, clamp method, cure and through-bolt details: U. Feet shown symbolically; actual compressed heights govern level and datum A.',9.7)
text(617,392,'SUPPORT GEOMETRY / CENTERED POINT-FOOT EXAMPLE',11,'Bold',BLUE)
formula(617,363,'a = D_foot / (2 sqrt(2))',13)
para(617,347,565,'For D_foot = 13-14 in, the square side-to-center distance is 4.60-4.95 in. This is smaller than the base radius. Use actual contact patches and loaded compliance for the final support hull.',10.5)
line(42,248,1182,248,GRID,1)
note(42,225,548,'PRIMARY FRAME ATTACHMENT','Locate the spine shoe, backing structure and any braces from the reviewed frame joint. The circular base outline does not specify bolt centers. Include base bending, local bearing, pull-through and joint rotation.',RED)
note(617,225,565,'FIELD RECORD','Record each foot center (x, y), patch size, compressed height, fastener ID and mounting surface. Verify four contacts without rocking. Plot the loaded center-of-gravity projection on M03.',BLUE)
end()

# 07 - spine and forces
page(7,'FIRST-ORDER STATIC MODEL / NO WOOD GRADE OR CONNECTION CAPACITY HAS BEEN ASSIGNED')
panel(42,322,530,337,'01  /  SPINE CROSS-SECTION',True)
rect(208,411,116,145,AMBER,Color(.98,.95,.86),1.5)
line(266,368,266,608,BLUE,.6,[8,3,2,3]);line(144,483.5,473,483.5,BLUE,.6,[8,3,2,3])
circle(444,483.5,4,NAVY,NAVY)
dimh(208,324,590,556,556,'d toward strings / U')
dimv(411,556,178,208,208,'b across array / U')
dimh(324,444,379,411,483,'c from face / N')
dimh(266,444,345,411,483,'e = d/2 + c')
text(385,526,'String plane',10,'Bold')
text(282,464,'axis B',9,color=TEAL)
panel(589,322,593,337,'02  /  UPPER AND LOWER ACTIONS ON THE FRAME',True)
rect(739,384,28,196,AMBER,Color(.98,.95,.86),1.5)
for yy in [390,567]:line(753,yy,922,yy,NAVY,2)
line(922,390,922,567,NAVY,.8,[4,3])
arrow(922,612,922,571,RED,2);arrow(922,345,922,386,RED,2)
text(947,586,'Top: P downward',11,color=RED)
text(947,361,'Bottom: P upward',11,color=RED)
dimh(753,922,465,420,420,'e from section axis')
para(612,635,537,'Paired forces close through the frame. Vessel is outside this force loop.',9.5)
text(632,341,'Joint-to-joint span L_a is U; do not substitute speaking length.',9.4)
formula(42,290,'P = sum(T_i)    M_x = -sum(y_i T_i)    M_y = sum(x_i T_i)',12)
para(42,271,1140,'Signs shown for downward forces at the upper connection; lower forces reverse. A moved force requires the equivalent couple. Do not replace e with d/2 merely because a bracket touches the spine face. [W2]',10.4)
formula(42,222,'A = b d    I_x = b d^3/12    S_x = b d^2/6',12)
formula(42,193,'sigma = P/A +/- |M_x|/S_x   (one-axis model)',12)
formula(42,163,'S_x/A = d/6  (rectangular-section kern)',12)
para(637,225,545,'Use measured net sections and both bending axes when needed. Holes, defects, moisture, grade, bearing, restraint, creep and connection rotation remain part of review. Full 2 x 3 in and dressed 1.5 x 2.5 in sections are examples, not interchangeable stock.',10.5)
para(42,134,545,'Formula gives stress demand only; no allowable stress is selected here.',9.5,color=RED)
end()

# 08 - upper interface
page(8,'UPPER JOINT CONCEPT / FASTENER CENTERS, SIZES AND REACTION GEOMETRY UNRESOLVED')
panel(42,265,700,394,'01  /  UPPER HEAD-BLOCK INTERFACE, SIDE SECTION',True)
rect(266,328,68,246,AMBER,Color(.98,.95,.86),1.5)
rect(244,447,13,143,RED,None,1,[4,3])
rect(344,447,95,143,RED,None,1,[4,3])
for yy in [480,550]:
    line(231,yy,453,yy,RED,1.4,[4,3]);circle(452,yy,7,RED,white)
rect(439,489,159,27,NAVY,white,1.5)
circle(577,539,12,NAVY,white)
line(577,539,594,526,NAVY,1.5);line(594,526,598,489,NAVY,1.2)
line(598,489,598,305,NAVY,1.4)
arrow(598,407,598,347,RED,2)
rect(548,477,79,88,BLUE,None,1,[5,3])
dimv(480,550,205,244,244,'g_z U')
leader([(257,573),(151,598)],'Back plate footprint U\nFull bearing / access',65,633,169,RED)
leader([(390,576),(440,609)],'Head block / shoulder U\nPositive vertical reaction',429,633,270,RED)
leader([(585,550),(647,575)],'Tuner winding\nclearance U',622,598,101)
text(66,281,'Dashed red components reserve a review zone; they are not fabrication geometry.',9.5,color=RED)
text(768,637,'INTERFACE REGISTER',12,'Bold',BLUE)
table(768,617,[65,349],['ID','REQUIRED INPUT'],[
('U01','Tuner model, string end type, mounting thickness and fastener drawing.'),
('U02','String run from winding post to nut; break angle and individual support reactions.'),
('U03','Head block and shoulder geometry, grain, contact area and slip restraint.'),
('U04','Bolt diameter, gauge along z, hole fits, end/edge margins and backing plate.'),
('U05','Coupled bolt tension/shear, prying, bearing, splitting, net section and rotation.'),
('U06','Guard, winding tool and string replacement swept envelopes.')],10,35)
note(42,233,700,'FORCE RESOLUTION AT A BEARING','At a nut or bridge, use the vector sum of the tensions in the adjacent string segments. The bearing reaction is not automatically equal to one string tension. The total upper subassembly still transfers the full string resultant into the frame.',BLUE)
note(768,218,414,'DETAIL STATUS','The PDF CX-1 hardware remains a candidate. No drill diameter, torque, metal grade substitution or operating load is released on this sheet.',RED)
end()

# 09 - lower connection
page(9,'LOWER JOINT CONCEPT / CLOSE STRING FORCES THROUGH THE FRAME')
panel(42,274,700,385,'01  /  LOWER ANCHOR, SIDE SECTION',True)
rect(256,379,68,235,AMBER,Color(.98,.95,.86),1.5)
rect(225,360,124,69,RED,None,1.2,[4,3])
rect(185,340,440,19,NAVY,white);rect(185,321,440,19,NAVY,white)
rect(203,302,38,19,TEAL,white);rect(569,302,38,19,TEAL,white)
rect(347,399,72,129,RED,None,1.2,[4,3])
rect(419,440,176,25,NAVY,white,1.5)
line(582,465,582,596,NAVY,1.6);circle(582,450,5,NAVY,white)
arrow(582,514,582,568,RED,2)
rect(227,399,13,129,RED,None,1.2,[4,3])
for yy in [420,501]:line(215,yy,431,yy,RED,1.3,[4,3])
rect(546,427,63,50,BLUE,None,1,[5,3])
leader([(320,386),(431,373)],'Frame shoe / base connection U',429,390,254,RED)
leader([(528,451),(484,543)],'Lower string termination U\nBall end / hitch / bushing',406,576,280)
leader([(227,488),(121,535)],'Backing plate\nand bolt group U',63,570,145,RED)
text(60,283,'Shoe and joint zones are symbolic. Vessel cradle is shown separately below.',9.6)
text(768,635,'LOWER END IS A SEPARATE REVIEW',12,'Bold',BLUE)
y=note(768,608,414,'L01  TERMINATION','Select compatible ball-end, loop or hitch geometry. Resolve local bearing, pull-through, tear-out, bend radius and broken-end containment.')
y=note(768,y,414,'L02  LOWER JOINT','Review the upward string force, eccentric couple and transverse bar bending. An inverted upper sketch does not prove identical contact or prying behavior.')
y=note(768,y,414,'L03  BASE CLOSURE','Include the actual shoe, backing members and plate-to-base load transfer. Avoid counting the full internal string force as additional external weight.')
note(768,y,414,'L04  RESTRAINT','Review anti-tip anchorage under its own external load cases. It is not automatically provided by the string-anchor bolts.',RED)
# Small separate shell cradle diagram.
rect(117,139,511,16,NAVY,white)
ellipse(185,167,219,78,BLUE,None,1.4)
rect(187,157,51,18,TEAL,white);rect(352,157,51,18,TEAL,white)
arrow(220,212,220,179,TEAL,1.4);arrow(370,212,370,179,TEAL,1.4)
text(71,249,'02  /  INDEPENDENT VESSEL SUPPORT CONCEPT',11,'Bold',BLUE)
text(419,195,'Vessel weight',10,'Bold',TEAL)
para(768,219,414,'The vessel is supported for its own weight and motion using padded contact. No part of the shell, neck or rim is a string-force reaction member. Support-pad sizes and preload remain U.',10.5,color=TEAL)
end()

# 10 - anchor bar
page(10,'STRING CENTERLINE LAYOUT / HOLE AND HARDWARE DETAILS NOT RELEASED')
panel(42,343,754,316,'01  /  BAR FRONT ELEVATION (x-z)',True)
xx=143;yy=466;sc=45
rect(xx,yy,12*sc,1.5*sc,NAVY,white,1.7)
for k in range(5):
    xc=xx+(2+2*k)*sc
    circle(xc,yy+.75*sc,5,BLUE,white,1)
    line(xc,yy-13,xc,yy+90,BLUE,.6,[6,3,2,3])
    text(xc,yy+15,f'S{k+1}',8.8,'Mono',BLUE,'center')
    arrow(xc,yy+124,xc,yy+82,RED,1.1)
dimh(xx,xx+12*sc,390,yy,yy,'L_bar = 12 in / S2 CX-1 CANDIDATE')
dimh(xx+2*sc,xx+10*sc,579,yy+68,yy+68,'4 spaces x 2 = 8 in N')
dimh(xx,xx+2*sc,429,yy,yy,'a_end = 2 C')
dimh(xx+10*sc,xx+12*sc,429,yy,yy,'a_end = 2 C')
text(62,357,'Centerlines only. s = 2 in N; planning range 1.5-2.25 in. All drilling and terminations U.',9.4,color=RED)
panel(813,343,369,316,'02  /  SECTION (y-z)')
rect(949,434,42,126,AMBER,white,1.5)
dimh(949,991,391,434,434,'t_y U')
dimv(434,560,1061,991,991,'h_z U')
arrow(971,583,971,622,BLUE,1);text(986,604,'+z',10)
arrow(995,492,1115,492,BLUE,1);text(1081,508,'+y',10)
text(832,358,'Section orientation must be declared.',9.5)
text(42,315,'GEOMETRY AND BENDING CHECKS',12,'Bold',BLUE)
formula(42,288,'L_bar = (N - 1)s + 2 a_end = 8 + 2 a_end',12)
para(42,271,754,'Neither 10, 11 nor 12 in is a universal required length. End allowance follows the actual termination, hole, material, load direction and review. A 12 in bar leaves 2 in at each end geometrically; that does not establish a capacity.',10.3)
formula(42,217,'M_left = 16.2525(4 - .75) + 13.0187(2 - .75)',11.6)
formula(42,193,'       = 69.09 lbf-in  C   (S2 states 113)',11.6)
para(42,179,754,'This example assumes continuous support across a centered 1.5 in width and vertical string forces. Right side: 68.47 lbf-in. Change the support or force direction and recalculate. No net-section stress or deflection result is certified.',9.8)
formula(813,305,'S_y = t_y h_z^2 / 6',12)
para(813,284,369,'For vertical loads on an x-spanning bar, h_z is the bending depth. For the illustrated candidate t_y = 0.5 and h_z = 1.5 in: S_y = 0.1875 in^3 before holes.',10.3)
para(813,205,369,'A 1.5 in-high bar cannot contain two z-spaced bolt centers 1.5 in apart with positive margins. A separately sized connection block or revised geometry is required for that proposal.',10.3,color=RED)
end()

# 11 - vessel and top
page(11,'INDEPENDENT SHELL SUPPORT / AIR GAP AND ASSEMBLY PATH MUST BE MEASURED')
panel(42,288,558,371,'01  /  PROFILE STATIONS',True)
cx=320
vessel(cx,331,263,160)
for i,(yy,half) in enumerate([(348,65),(401,84),(455,96),(509,84),(574,48)]):
    line(cx-half,yy,cx+half,yy,TEAL,.8)
    text(78,yy-3,f'z{i}',10,'Mono',TEAL)
    line(105,yy,cx-half-9,yy,TEAL,.6,[3,3])
line(cx,316,cx,613,BLUE,.6,[8,3,2,3])
text(389,598,'Mouth ID / OD U',10,color=BLUE)
dimh(272,368,616,594,594,'MOUTH U')
text(68,301,'Add stations at every hardware level, shoulder and narrow section.',9.5)
panel(618,451,564,208,'02  /  TOP PLATE AND ANNULAR GAP')
ellipse(761,569,286,14,NAVY,white,1.3)
line(838,510,838,543,BLUE,2);line(970,510,970,543,BLUE,2)
line(838,543,970,543,BLUE,1.1)
rect(894,526,17,43,RED,None,1,[3,3])
dimv(543,569,1089,1047,1047,'g_top N')
text(640,617,'Top diameter 16 in N; permitted planning range 14-18 in.',10.3)
para(640,498,520,'Gap g_top = 1.5 in N, planning range 1-2 in. Captive removable mount U. Keep shell and plate from unintended hard contact.',10.1)
panel(618,288,564,147,'03  /  PADDED CONTACT DETAIL')
line(858,320,888,397,BLUE,3)
line(869,322,899,399,TEAL,8)
line(881,318,912,397,NAVY,2)
leader([(903,371),(966,378)],'Pad + strap / cleat\npressure and restraint U',975,402,181)
text(642,325,'Shell',10,color=BLUE);line(677,329,860,345,BLUE,.7)
line(42,266,1182,266,GRID,1)
note(42,244,558,'FIT RECORD','Measure wall thickness, inside boundary, mouth, base, material, mass and defects. Record the occupied hardware envelope and required movement allowance at each station. Do not infer inside diameter from outside appearance.',BLUE)
note(618,244,564,'SUPPORT / ACCESS RECORD','Pad area, preload, attachment method and removal path are U. Avoid point loads on glass; never drill tempered glass. Confirm guard and tuner access without contacting the shell. [S1 sections 4-5]',BLUE)
para(42,137,1140,'Cavity volume remains undetermined: V = integral A(z) dz requires measured internal areas and integration limits. Opening shape, gaps and acoustic coupling are also unmeasured; no Helmholtz frequency or resonant performance is assigned.',10.3,color=RED)
end()

# 12 - strings
page(12,'EX-B1-R1 / RECOMPUTED CANDIDATE ONLY / NO STRING PURCHASE OR OPERATING SET IS RELEASED')
units=[.00012671,.00007177,.00004342,.00003190,.00002215]
notes=['A2','C3','E3','G3','C4'];midi=[45,48,52,55,60]
freq=[440*2**((m-69)/12) for m in midi]
ts=[u*(64*f)**2/386.4 for u,f in zip(units,freq)]
mus=[u*.45359237/.0254*1000 for u in units]
products=['NW026 / .026 wound','LE018 / PL018 / .018 plain','LE014 / PL014 / .014 plain','LE012 / PL012 / .012 plain','LE010 / PL010 / .010 plain']
rows=[]
for i in range(5):rows.append((f'S{i+1}',notes[i],f'{freq[i]:.4f}',products[i],f'{units[i]:.8f}',f'{mus[i]:.4f}',f'{ts[i]:.2f}',f'{ts[i]*4.4482216152605:.2f}'))
para(42,651,1140,'Common assumptions: L = 32.00 in (0.8128 m), A4 = 440 Hz equal temperament, flexible-string model, source-PDF unit weights. Product names and aliases are carried from S2; their current equivalence and usable string length require maker confirmation.',10.6)
table(42,599,[43,47,102,341,150,125,107,125],['ID','NOTE','f / Hz','SOURCE PRODUCT LABEL','UW / lb/in','mu / g/m','T / lbf','T / N'],rows,10,39)
rect(42,304,1140,44,stroke=TEAL,fill=PALE)
text(58,320,f'RECOMPUTED TOTAL: {sum(ts):.2f} lbf  /  {sum(ts)*4.4482216152605:.2f} N',15,'Bold',TEAL)
text(1159,321,'SOURCE PDF: 70.8 lbf rounded',10,'Mono',GRAY,'right')
formula(42,272,'T = mu (2Lf)^2',14)
formula(42,243,'T_lbf = UW (2 L_in f)^2 / 386.4',12)
formula(42,216,'1 lbf = 4.448221615 N',11)
para(42,199,550,'The inherited 386.4 convention is used to reproduce the maker-style calculation in S2. Calculation precision does not increase confidence in the transcribed UW. [S2 pp1-5; W1]',9.8)
note(623,278,559,'DATA THAT STILL NEED CONFIRMATION','Exact product, construction, unit weight, total length, winding/post fit, termination, usable pitch range and individual reviewed limit. Tuner and joint review must cover the actual string path.',RED)
para(623,170,559,'20 lbf/string and 100 lbf total remain planning ceilings. A calculated candidate below them is not an authorized operating set. Use the lower reviewed operating limits; missing data leave the assembly untensioned.',10.2,color=RED)
end()

# 13 - loading worksheet
page(13,'DEMAND CALCULATIONS ARE CONDITIONAL / ALL CAPACITY AND DEFLECTION FIELDS REMAIN U')
text(42,649,'CASE REGISTER',12,'Bold',BLUE)
loadrows=[
('LC0','Untensioned assembly','Self-weight, handling, shell supports, feet and restraint installation.'),
('LC1','All five at reviewed targets','Use each T_i, x_i and y_i; axial force and both bending moments.'),
('LC2','Staged tuning / one-sided loading','Check maximum imbalance during the declared tuning sequence.'),
('LC3','One string slack or broken','Residual static forces plus separately reviewed release/transient effects.'),
('LC4','Tuning torque / handling','Resolve tuner torque, operator forces and accessory loads.'),
('LC5','Tip / slip / restraint','External loads, mass, CG and restraint geometry. See M03.')]
table(42,631,[61,189,462],['CASE','CONFIGURATION','CHECK'],loadrows,10,34)
panel(775,359,407,300,'CONDITIONAL NUMERIC SCREEN')
formula(793,610,'P = 70.8354 lbf',13)
formula(793,581,'e = 2.5/2 + 3 = 4.25 in',11.5)
formula(793,552,'|M_x| = 301.05 lbf-in',11.5)
formula(793,523,'sum(x_i T_i) = -0.78',11.5)
text(793,505,'lbf-in, for x = -4, -2, 0, +2, +4 in',9.5)
para(793,483,371,'Illustrative actual section b = 1.5, d = 2.5 in: A = 3.75 in^2; S_x = 1.5625 in^3. First-order one-axis front stress = 211.56 psi; back stress = 173.78 psi tension.',10)
para(793,395,371,'This is a demand example, not a rating for a nominal 2 x 3 or a drilled joint.',10,color=RED)
text(42,313,'COMPLETE BEFORE A FABRICATION OR TENSIONING RELEASE',12,'Bold',BLUE)
table(42,297,[192,250,252,243,203],['ITEM','MEASURE / DEFINE','REVIEW METHOD','LIMIT / RESULT','EVIDENCE ID'],[
('Spine / frame','Actual b, d, span, defects','Net section; stability; creep','U / U','U'),
('Bars / head blocks','Material, orientation, holes','Bending; shear; deflection','U / U','U'),
('Connections','Bolts, bearing faces, gauge','Combined actions; slip; splitting','U / U','U'),
('Deflection / clearance','Initial shape; joint motion','Loaded motion + residual set','U / U','U'),
('Strings / tuners','Product and installation','Target, safe range, local forces','U / U','U')],9.7,30)
end()

# 14 - stability
page(14,'EXTERNAL EQUILIBRIUM / STRING TENSION IS INTERNAL TO THE CLOSED ASSEMBLY')
panel(42,313,562,346,'01  /  PLAN: ACTUAL FOOT-CONTACT HULL',True)
cx,cy=322,477
circle(cx,cy,132,GRID,None,1)
rect(cx-91,cy-91,182,182,TEAL,None,1.6)
for dx in [-91,91]:
    for dy in [-91,91]:circle(cx+dx,cy+dy,10,TEAL,white,1.5)
circle(cx+25,cy+21,5,RED,RED)
arrow(cx+25,cy+21,cx+91,cy+21,RED,1.3)
text(cx+38,cy+39,'b_edge U',9.5,color=RED)
text(cx-5,cy-7,'CG projection U',10,color=RED)
text(65,330,'Find the minimum distance to every relevant pivot edge.',9.5)
panel(621,313,561,346,'02  /  SIDE: WEIGHT, LOAD AND RESTRAINT',True)
line(671,363,1141,363,NAVY,1.4)
rect(853,363,95,27,NAVY,white)
line(901,390,901,598,BLUE,2)
circle(901,480,6,RED,RED);arrow(901,480,901,402,RED,1.6)
text(916,434,'W',11,'Bold',RED)
arrow(901,576,1002,576,RED,1.5);text(1010,572,'F_ext U',10,color=RED)
line(708,363,708,620,GRAY,1.4)
line(708,595,901,536,TEAL,1.4,[6,3])
circle(708,595,4,TEAL,white);circle(901,536,4,TEAL,white)
text(721,618,'Wall attachment U',10,color=TEAL)
text(741,523,'Strap angle / slack U',9.5,color=TEAL)
dimv(363,480,1084,948,901,'h_CG U')
dimh(901,948,338,363,363,'b U')
text(42,286,'STATIC SCREEN / NO SLIDING / NO RESTRAINT CONTRIBUTION',11,'Bold',BLUE)
formula(42,257,'F_ext h_load < W b_edge',13)
formula(42,226,'tan(theta_tip) = b_edge / h_CG',12)
para(42,211,562,'Use the actual direction of loading and the nearest relevant pivot edge. The old 10 degree tilt is a calculation example only; it is not an instruction to tilt the apparatus.',10.4)
note(621,284,561,'RESTRAINT DEMAND','Calculate using the actual attachment coordinates, allowable load directions, wall/substrate anchorage, slack and engagement path. Dynamic engagement cannot be inferred from a static label or a generic 200 lbf rating.',BLUE)
para(621,171,561,'Record mass and CG in x, y and z, foot contact behavior, external test load, angle, force, fixture and abort condition. Slip and tip require separate checks. No anti-tip rating is assigned here.',10.4)
end()

# 15 - field measurements
page(15,'BLANK RECORDS ARE U / COMPLETE WITH UNITS, UNCERTAINTY AND EVIDENCE')
text(42,649,'CONFIGURATION ID: ____________________    DATE: ____________________    MEASURED BY: ____________________',11,'Mono')
text(42,617,'01  /  VESSEL AND OCCUPIED ENVELOPE',12,'Bold',BLUE)
vrows=[(s,'','', '', '', '') for s in ['Mouth / entry','Upper anchor','Upper shoulder','Maximum belly','Lower shoulder','Lower anchor','Support / base']]
table(42,601,[156,98,220,218,248,200],['STATION','z FROM A','INNER PROFILE / ID','HARDWARE ENVELOPE','MIN CLEARANCE / MOTION','PHOTO / METHOD'],vrows,9.5,34)
text(42,301,'02  /  DATUM AND STOCK CLOSURE',12,'Bold',BLUE)
table(42,285,[215,191,141],['ITEM','ACTUAL / UNITS','EVIDENCE'],[
('Spine b x d / length','',''),('Section orientation / grain','',''),('Base + feet stack height','',''),('Upper / lower bearing z','',''),('Overall H / top gap','','')],9.5,29)
text(616,301,'03  /  CONNECTION AND SUPPORT INPUTS',12,'Bold',BLUE)
table(616,285,[249,164,153],['ITEM','ACTUAL / UNITS','EVIDENCE'],[
('Bar / block / backing sizes','',''),('Hole axes / diameter / margins','',''),('Bolt group gauge / material','',''),('Foot coordinates / patches','',''),('Mass / CG / restraint geometry','','')],9.5,29)
end()

# 16 - assembly inspection
page(16,'SEQUENCE FROM S1 / CONDITIONAL ON DIMENSIONAL AND STRUCTURAL REVIEW')
steps=[
('01','Close the dimensional model','Complete Q01. Check vessel entry path, all occupied sections, vertical stack and service access. Retain N values only if the measured arrangement supports them.'),
('02','Complete the structural review','Select actual members, connections, strings and reviewed operating limits. Resolve D03-D05 and M02-M03; issue a separate cutting and drilling schedule.'),
('03','Dry-fit the frame','After review, fit base, spine, head block and lower anchor without the vessel. Use the reviewed bolts, backing members and braces. Record tightening requirements.'),
('04','Fit supports and protection','Establish foot contacts and reviewed restraint. Fit independent padded vessel support, nut/bridge, guards and cable strain relief. Confirm every clearance again.'),
('05','Install and tune to reviewed targets','Use the reviewed sequence. Inspect near 25%, 50%, 75% and 100% of those targets, not automatically the planning ceiling. Stand out of the string plane; wear eye protection.'),
('06','Observe and record','After load review, observe at operating tension for 30 min; measure loaded deflection and unloaded recovery. Compare with the predeclared limits. This is not proof-load certification.'),
('07','Fit the removable top and measure','Fit the documented captive mount once frame stability is established. Record the actual coupling and proceed to the passive acoustic baseline on Q03.')]
yy=649
for n,title,body in steps:
    circle(63,yy-9,18,BLUE,PALE,1)
    text(63,yy-13,n,11,'Mono',BLUE,'center')
    text(98,yy,title.upper(),11.2,'Bold')
    para(98,yy-10,1084,body,10.1)
    yy-=69
rect(42,111,1140,49,stroke=RED,fill=HexColor('#FFF5F3'))
text(56,140,'STOP / ABORT',10.5,'Bold',RED)
para(185,152,977,'Cracking, progressive movement, slip, permanent deformation, unstable footing, loss of clearance or vessel contact. Remove load using the reviewed safe method; record the condition and reassess the affected joint.',10,color=RED)
end()

# 17 - acoustic setup & release
page(17,'PASSIVE BASELINE / COMPLETE RECORD BEFORE CLAIMING A MEASURED RESULT')
panel(42,375,551,284,'01  /  REPEATABLE MEASUREMENT SETUP',True)
front(243,406,.45,False)
circle(247,519,5,TEAL,white,1.5);circle(281,486,5,TEAL,white,1.5)
line(286,486,392,450,TEAL,1.2)
rect(392,415,155,42,NAVY,white)
text(469.5,438,'Battery recorder',10,'Bold',align='center')
text(469.5,422,'fixed gain / raw files',8.8,align='center')
arrow(103,501,194,501,TEAL,1.3)
text(69,528,'Repeatable',9.7);text(69,514,'excitation',9.7)
text(340,600,'Fixed sensor mounts',10,'Bold',TEAL)
para(340,584,231,'Retain a simultaneous input or reference. Mark pluck/tap position and displacement. Record room and instrument configuration.',9.8)
text(617,649,'MEASUREMENT REGISTER / S1 T0-T8',12,'Bold',BLUE)
table(617,632,[49,166,350],['TEST','ACTION','RECORD / INTERPRETATION'],[
('T0-T2','Inspect / observe / assess','Complete reviewed mechanical and stability criteria first.'),
('T3','Component tap map','Damp strings; fixed mounts and repeatable excitation.'),
('T4','Individual strings','Pitch, harmonics, drift and defined 10 dB decay interval.'),
('T5','Transfer response','H = Y/F only with measured input; otherwise response ratio.'),
('T6','Airflow map','Tufts clear of strings; optional guarded external fan >=12 in away.'),
('T7','Room sweep','External speaker >=3 ft away; 20-200 Hz; predeclared SPL ceiling.'),
('T8','Phase 2 only','After T0-T7 pass; separate reassessment and S1 electrical limits.')],9.2,30)
formula(42,345,'Q = (2 pi / ln(10)) f0 t_10dB',12)
para(42,329,551,'Single isolated mode with exponential amplitude decay only. Record fit band, interval, noise floor and uncertainty. Unresolved beating, clipping, gain changes or multiple modes prevent a single-mode Q estimate.',10)
para(42,250,551,'Keep raw recordings and configuration ID, date/time, string identities, pitches/tensions, sample rate, gain, sensors, excitation, room state, temperature, anomalies and stop reason. Start with at least three repeats; vary one factor per comparison.',10)
text(617,290,'COMPLETION RECORD / UNEXECUTED',11.5,'Bold',RED)
table(617,276,[224,162,179],['RELEASE ITEM','STATUS','REVIEW / DATE'],[
('Measured geometry','UNRESOLVED',''),('String + connection limits','UNRESOLVED',''),('Stability + restraint','UNRESOLVED',''),('Fabrication / load / acoustics','NOT EXECUTED','')],9.5,29)
para(42,145,551,'Phase 2 source limit: isolated fused 12-24 VDC, <=30 W, no mains inside assembly; mount temperature rise <=10 C after 10 min. No powered exciter is part of this baseline.',9.5)
end()

c.save()
# Basic text placement check; visual inspection of rendered sheets is still required.
bad=[r for r in checks if r[1]<23 or r[3]>1201 or r[2]<24 or r[4]>769]
(OUT/'source'/'layout_checks.json').write_text(json.dumps({'text_items':len(checks),'outside_page_border':bad},indent=2))
numeric={'configuration':'EX-B1-R1','status':'conditional candidate; not selected operating set',
    'source_UW_status':'transcribed from supplied PDF; current maker values not reconfirmed',
    'L_in':32,'frequency_Hz':freq,'UW_lb_in':units,'mu_g_m':mus,'tension_lbf':ts,
    'total_lbf':sum(ts),'total_N':sum(ts)*4.4482216152605,
    'left_bar_moment_lbf_in':ts[0]*3.25+ts[1]*1.25,
    'right_bar_moment_lbf_in':ts[4]*3.25+ts[3]*1.25,
    'string_only_clear_ID_example_in':2*(math.hypot(4,4.5)+1),
    'bar_clear_ID_example_in':2*(math.hypot(6,4.75)+1)}
(OUT/'source'/'calculation_record.json').write_text(json.dumps(numeric,indent=2))
print(json.dumps({'pdf':str(PDF),'pages':len(SHEETS),'text_items':len(checks),'outside_border':bad},indent=2))
