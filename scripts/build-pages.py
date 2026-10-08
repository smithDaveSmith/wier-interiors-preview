from pathlib import Path
import re,json,html,shutil
ROOT=Path(__file__).resolve().parent.parent
DIST=ROOT/'dist'
e=html.escape
SITE_ORIGIN=json.loads((ROOT/'source/site-settings.json').read_text())['origin'].rstrip('/')
home=(ROOT/'source/home.html').read_text()
head=re.search(r'<head>(.*?)</head>',home,re.S).group(1).replace('href="styles.css"','href="/styles.css"').replace('src="script.js"','src="/script.js"')
footer=re.search(r'<footer.*?</footer>',home,re.S).group(0)
base='https://www.weirinteriors.ie'
routes=['about','decor-fabrics','interior-design','refurbishments','gallery-showroom','contact','privacy-policy']
for route in sorted(routes,key=len,reverse=True):
 footer=footer.replace(base+'/'+route, '/'+route)
footer=re.sub(r'href="(/(?:about|decor-fabrics|interior-design|refurbishments|gallery-showroom|contact|privacy-policy)(?:/\d+)?)"',r'href="\1/"',footer)
footer=footer.replace('class="footer-wordmark" href="#top"','class="footer-wordmark" href="/"').replace('Official contact page','Contact us').replace('Official privacy policy','Privacy & this preview')
mobile='<div class="mobile-contact"><a href="tel:+35316010972">Call the showroom</a><a href="/contact/">Discuss your project</a></div>'
COLLECTIONS={28:('New arrivals','Furniture, lighting and decorative details from the original showroom collection. Please enquire about current availability.'),20:('Curtains & upholstery','Fabric combinations, window dressings and upholstery ideas from the original collection.'),26:('Wallpaper','Pattern, texture and colour for your walls. Browse the original wallpaper collection and discuss samples in the showroom.'),21:('Furniture','Furniture and room-setting examples from the original showroom gallery. Contact us for availability and prices.'),22:('Bespoke headboards','Made-to-order headboard examples from the original collection. Talk to us about fabrics and your room.'),19:('Cushions','A closer look at cushions, fabrics and finishing touches from the original collection.'),24:('Mirrors','Mirror examples from the original showroom collection. Contact us for prices or visit the showroom.'),16:('Accessories & candles','Accessories and Max Benjamin candles from the original collection. Enquire about current availability.'),23:('Lighting','Lighting examples from the original showroom collection. Visit Lucan Village to explore the range.'),17:('Artwork','Artwork from the original showroom collection. Ask us about pieces for your space.'),18:('Clocks','Clock designs from the original showroom collection. Enquire about availability and prices.'),25:('The Sandymount project','Project photographs from the original Sandymount gallery, with the separately named Westmeath photographs identified below.')}
DATA=json.loads((ROOT/'source/gallery-data.json').read_text()) if (ROOT/'source/gallery-data.json').exists() else []
PHOTOS={gid:[x for x in DATA if x['collection']==gid and x['ok']] for gid in COLLECTIONS}

def link(url,text,cls='text-link'):return f'<a class="{cls}" href="{url}">{text}</a>'
def header(route):
 def a(url,text,extra=''):
  active=' aria-current="page"' if route==url else ''
  return f'<a href="{url}"{active}{extra}>{text}</a>'
 service_active=' active-services' if route in ['/decor-fabrics/','/interior-design/','/refurbishments/'] else ''
 return f'''<a class="skip-link" href="#main">Skip to content</a><div class="concept-bar"><span>Independent design concept · Not the official website</span><a href="https://www.weirinteriors.ie/">Visit official website</a></div><header class="header"><a class="brand" href="/" aria-label="Weir Interiors home"><img src="/assets/logo.png" alt="Weir Interiors" width="175" height="92"></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="navigation">Menu <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Main navigation">{a('/','Home')}{a('/about/','Our story')}<details class="service-menu{service_active}"><summary>Our services</summary><div>{a('/decor-fabrics/','Décor & fabrics')}{a('/interior-design/','Interior design')}{a('/refurbishments/','Refurbishments')}</div></details>{a('/gallery-showroom/','Gallery & showroom')}{a('/contact/','Discuss your project',' class="button button-small"')}</nav></header>'''
def crumb(name,parent=None):
 mid=f'<li><a href="{parent[0]}">{e(parent[1])}</a></li>' if parent else ''
 return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>{mid}<li aria-current="page">{e(name)}</li></ol></nav>'
def image(src,alt,w,h,cls='',eager=False):
 return f'<img class="{cls}" src="{src}" alt="{e(alt)}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}"'+(' fetchpriority="high"' if eager else '')+'>'
def page(title,description,route,content):
 h=re.sub(r'<title>.*?</title>',f'<title>{e(title)} | Weir Interiors — Concept</title>',head)
 h=re.sub(r'<meta name="description"[^>]*>',f'<meta name="description" content="{e(description)}">',h)
 page_key=route.strip('/').replace('/','-') or 'home'
 text=f'<!doctype html><html lang="en-IE"><head>{h}</head><body id="top" data-page="{e(page_key)}">{header(route)}<main id="main">{content}</main>{footer}{mobile}</body></html>'
 # Explicit site destinations also work when the concept is viewed in an embedded preview.
 text=re.sub(r'(href|data-full)="(/[^\"]*)"',lambda m:f'{m.group(1)}="{SITE_ORIGIN}{m.group(2)}"',text)
 target=DIST/route.strip('/')/'index.html' if route!='/' else DIST/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
def cta(title='Let’s talk about your home.',text='Tell us what you have in mind, and we’ll discuss the right place to start.'):
 return f'<section class="page-cta section"><div><p class="eyebrow">YOUR NEXT CHAPTER</p><h2>{title}</h2><p>{text}</p></div><div>{link("/contact/","Discuss your project","button button-light")}{link("tel:+35316010972","Call 01 601 0972")}</div></section>'
def pagehero(name,kicker,title,description,src,alt,w,h):
 return crumb(name)+f'<section class="page-hero"><div><p class="eyebrow">{kicker}</p><h1>{title}</h1><p>{description}</p>{link("/contact/","Discuss your project","button")}</div><figure>{image(src,alt,w,h,eager=True)}</figure></section>'
def textsection(kicker,title,paragraphs):
 return f'<section class="section prose-split"><div><p class="eyebrow">{kicker}</p><h2>{title}</h2></div><div class="prose">'+''.join(f'<p>{p}</p>' for p in paragraphs)+'</div></section>'
def scope(title,items):
 return f'<section class="section scope-section"><p class="eyebrow">THE DETAILS, CONSIDERED</p><h2>{title}</h2><div class="scope-grid">'+''.join(f'<article><h3>{t}</h3><p>{d}</p></article>' for t,d in items)+'</div></section>'
def collectioncards(ids,heading='h3'):
 result='<div class="collections-grid">'
 for gid in ids:
  photos=PHOTOS[gid];cover=photos[0] if photos else None
  # Use a known room setting for curtains and upholstery rather than a catalogue cutout.
  if gid==20:cover=next((p for p in photos if 'RomoOxleySHOT05BENCH' in p['original_filename']),cover)
  pic=image(cover['thumb'],COLLECTIONS[gid][0]+' — original collection example',cover['thumbWidth'],cover['thumbHeight']) if cover else ''
  result+=f'<a class="collection-tile" href="/gallery-showroom/{gid}/"><div>{pic}</div><{heading}>{e(COLLECTIONS[gid][0])}</{heading}><span>{len(photos)} photographs · Browse collection</span></a>'
 return result+'</div>'
def collectionsection(title,ids):return f'<section class="section related-gallery"><div class="work-heading"><div><p class="eyebrow">TAKE A CLOSER LOOK</p><h2>{title}</h2></div>{link("/gallery-showroom/","All collections")}</div>{collectioncards(ids)}</section>'

# Homepage: keep its composition, replace old-site destinations and use a true contact page.
content=re.search(r'<main id="main">(.*?)</main>',home,re.S).group(1)
contact=re.search(r'<section class="contact section".*?</section>',content,re.S).group(0)
(ROOT/'source/contact-section.html').write_text(contact)
content=content.replace(contact,cta('What are you <em>imagining?</em>','A room refresh, new curtains or a bigger change. Tell us what you have in mind.'))
for route in sorted(routes,key=len,reverse=True):content=content.replace(base+'/'+route,'/'+route)
content=re.sub(r'href="(/(?:about|decor-fabrics|interior-design|refurbishments|gallery-showroom|contact)(?:/\d+)?)"',r'href="\1/"',content)
content=content.replace('src="assets/','src="/assets/').replace('srcset="assets/','srcset="/assets/').replace(', assets/',', /assets/')
content=content.replace('href="#contact"','href="/contact/"')
content=content.replace('id="top"','id="home-hero"')
page('Interior Design & Décor, Lucan, Dublin','Interior design, bespoke curtains and home refurbishment from Weir Interiors in Lucan, serving Dublin, Kildare, Meath and Wicklow.','/',content)

# About
body=pagehero('Our story','A LOCAL BUSINESS · SINCE 2010','A love of fabrics.<br>A feeling for <em>home.</em>','Founded by Sharon Carroll, Weir Interiors brings design advice, furnishings and refurbishment support together in the heart of Lucan Village.','/assets/showroom2.webp','Armchair, decorative lighting and patterned fabrics in the Weir Interiors showroom',768,768)
body+=textsection('THE STORY BEHIND WEIR','Personal, from<br><em>the beginning.</em>',["Sharon Carroll grew up as the daughter of a dressmaker, surrounded by fabrics, shopping trips to fabric stores and home decorating. That early interest led to studying at the Institute of Design in Dublin and establishing Weir Interiors in 2010.","What began with soft furnishings and room refreshes developed into a complete interior design service, including sourcing, refurbishment design and project management.","The showroom remains on Main Street in Lucan Village, beside Bank of Ireland: a place to look at samples, explore ideas and talk about the home you want to create."])
body+=scope('Homes change.<br><em>So do the things you need.</em>',[('A first home','Help bringing colours, fabrics and furnishings together as you make a new place your own.'),('A different stage of life','Reconsidering rooms as families grow, children move out or you settle into a new or holiday home.'),('Traditional or modern','Advice on the look, materials and room details that fit your style, space and budget.')])
body+=textsection('FROM AN IDEA TO THE DETAILS','Design advice.<br><em>Practical support.</em>',["We work with homeowners and landlords, from simple decoration to larger property changes. The service can include sourcing furnishings and materials and managing the tradespeople doing the work.","Our main service region covers Dublin, Kildare, Meath and Wicklow. We also welcome enquiries about larger projects elsewhere in Ireland.",link('/gallery-showroom/','Explore the showroom and project galleries')])
body+=cta();page('Our Story','Meet Weir Interiors, founded in 2010 by Sharon Carroll, with a showroom in Lucan Village, Dublin.','/about/',body)

# Decor
body=pagehero('Décor & fabrics','CURTAINS · TEXTURE · FINISHING TOUCHES','Small changes.<br><em>A different feeling.</em>','From bespoke curtains and cushions to wallpaper and upholstery, explore the details that can give a room a new character.','/assets/decor.webp','Floral upholstered sofa, cushions and furnishings from the original décor page',768,390)
body+=textsection('A ROOM REFRESH, YOUR WAY','Start with<br><em>what you love.</em>',["Sometimes a room needs a complete rethink. Sometimes the right fabric, curtain or piece of furniture is enough. We offer advice and help sourcing the colours, textures and details that work together.","You can explore fabric samples and catalogues in the Lucan showroom. If you would like to refresh a favourite piece of furniture, the service also includes upholstery and furniture painting."])
body+=scope('Fabrics, furnishings<br><em>and the finishing details.</em>',[('Bespoke curtains & window dressings','French pleat and goblet finishes, swags, tails and pelmets, as well as Roman and modern blinds.'),('Upholstery & furniture refresh','Fabric selection, upholstery and furniture painting for pieces you want to give a new look.'),('Cushions & headboards','Coordinating cushions and made-to-order headboard examples to explore for your room.'),('Wallpaper & floor coverings','Wall coverings, rugs and carpets that work with the rest of your interior.'),('Furniture & lighting','Help sourcing furniture and lighting, with examples in the original showroom collections.'),('Accessories & decorative pieces','Mirrors, artwork, clocks, glassware, candles and the smaller details that finish a space.')])
body+='<section class="section supplier-section"><p class="eyebrow">CHOICE, WITH GUIDANCE</p><h2>Find a fabric<br><em>that feels right.</em></h2><p>The original website lists ranges including Sanderson, Jane Churchill, GP & J Baker, Prestigious, Crowson, Romo and Villa Nova. Ask us about a particular fabric or explore samples in the showroom.</p><div class="supplier-names">Sanderson <span>Romo</span> Jane Churchill <span>Villa Nova</span> GP & J Baker</div></section>'
body+=collectionsection('Ideas in <em>texture and colour.</em>',[20,26,19,22]);body+=cta('A finishing touch<br><em>in mind?</em>','Tell us about your room, or visit the showroom to explore fabrics and samples.');page('Décor, Curtains & Fabrics','Explore bespoke curtains, blinds, upholstery, wallpaper and soft furnishings from Weir Interiors in Lucan.','/decor-fabrics/',body)

# Interior design
body=pagehero('Interior design','COLOUR · MATERIALS · A COMPLETE ROOM','Bring your home<br><em>into focus.</em>','Design advice and practical help with fabrics, furnishings, flooring and finishes, from a single room to your whole home.','/assets/design.webp','Patterned wallpaper, draped curtains and a table lamp from the original interior design page',768,390)
body+=textsection('SEE YOUR SPACE DIFFERENTLY','The right elements.<br><em>Working together.</em>',["A room’s atmosphere comes from the combination of its colours, textures and materials. We help you consider how those choices work together, whether you want a warm, cosy room or a more minimalist space.","The starting point is a consultation and quotation: looking at your interior, discussing the feeling you want to create and considering the scope of the changes.","With samples and catalogues available in the showroom, you can explore fabrics and colours alongside the other elements of the room."])
body+=scope('From the floor<br><em>to the finishing touch.</em>',[('Colours & wall finishes','Advice on paint, wallpaper and how the colours and materials in a room work together.'),('Fabrics & window dressings','Curtains, cushions and upholstered elements that complement the space.'),('Flooring & furniture','Help selecting and sourcing carpets, wooden floors, vinyl flooring and furniture.'),('Artwork & room details','Wall art and decorative elements considered as part of the complete interior.'),('Sourcing & coordination','Help finding products and materials, with project management of the tradespeople carrying out the work.'),('Larger changes','For extensions, conversions and structural alterations, explore the dedicated refurbishment service.')])
body+=textsection('ONE ROOM OR A WHOLE HOME','Your style.<br><em>Your starting point.</em>',["We work with different kinds of homes, from apartments and terraced properties to larger homes, holiday properties and listed buildings. The discussion starts with your space, style and budget.","The service can be a curtain-and-cushion refresh with new paint, or a more complete look at the interior. If you are planning major property changes, the refurbishment service brings design and project management together.",link('/refurbishments/','Explore home refurbishments')])
body+=collectionsection('A closer look at<br><em>spaces and details.</em>',[25,21,20]);body+=cta();page('Interior Design','Interior design advice, product sourcing and project management from Weir Interiors in Lucan, Dublin.','/interior-design/',body)

# Refurbishments
body=pagehero('Home refurbishments','DESIGN · SOURCING · PROJECT MANAGEMENT','A new chapter<br><em>for your home.</em>','Interior design and project management for renovations, extensions, conversions and structural changes.','/assets/renovation.webp','Interior planning drawings with colour and fabric samples from the original refurbishment page',768,390)
body+=textsection('RETHINKING WHAT IS POSSIBLE','A bigger change.<br><em>A considered plan.</em>',["Moving into a new home, adapting to a different stage of life or rethinking an older property can mean more than new decoration. We help you look at the whole interior and the ways it could work differently.","The refurbishment service can cover house extensions, loft conversions and structural alterations, alongside flooring, wall coverings, furniture and interior décor.","Weir Interiors can source the products and materials and oversee the tradespeople carrying out the work. The exact scope is discussed for your particular project."])
body+=scope('The work,<br><em>brought together.</em>',[('Extensions & conversions','Interior planning and project management for extensions and loft or basement conversions.'),('Structural alterations','Design consideration and project oversight for changes such as removing walls.'),('Kitchens & bathrooms','Coordination with kitchen and bathroom installers as part of a refurbishment.'),('Joinery & building work','Working with carpenters, joiners and structural building companies.'),('Services & decoration','Coordination with electricians, plumbers, painters and decorators.'),('Furniture & final details','Upholstery, furniture renewal, furnishings and room finishes as part of the interior.')])
body+=textsection('LOCAL ROOTS, LARGER PROJECTS','Tell us where<br><em>you want to begin.</em>',["Most work is in Dublin and the neighbouring counties of Kildare, Meath and Wicklow. The original website also describes larger renovation projects across Ireland.","Contact the team with your location, the rooms or property you want to change and the work you are considering. A consultation and free quote are offered; a fixed price or timescale is not published.",link('/contact/','Discuss your refurbishment')])
body+=collectionsection('Project <em>details.</em>',[25]);body+=cta();page('Home Refurbishments','Interior design and project management for home renovations, extensions and conversions from Weir Interiors in Lucan.','/refurbishments/',body)

# Gallery hub
body=crumb('Gallery & showroom')+'<section class="gallery-intro section"><p class="eyebrow">FABRICS · FURNISHINGS · PROJECTS</p><h1>A world of<br><em>possibilities.</em></h1><p>Browse the original showroom collections and project photographs. Find an idea that speaks to you, then talk to us about your home.</p><div class="gallery-tabs"><a href="#projects">Project photographs</a><a href="#collections">Showroom collections</a><a href="#visit">Visit the showroom</a></div></section>'
gallery_collections='<section class="section gallery-hub" id="collections"><div class="work-heading"><div><p class="eyebrow">LOOK, FEEL, EXPLORE</p><h2>The showroom <em>collections.</em></h2></div><p>Examples from the original website.<br>Enquire about availability and prices.</p></div>'
for name,ids in [('Fabrics & soft furnishings',[20,26,22,19]),('Furniture & decorative details',[21,23,24,17,18,16]),('New arrivals',[28])]:
 gallery_collections+=f'<div class="collection-group"><h3>{e(name)}</h3>'+collectioncards(ids,'h4')+'</div>'
gallery_collections+='</section>'
body+='<section class="section gallery-project" id="projects"><div><p class="eyebrow">PROJECT PHOTOGRAPHS</p><h2>Spaces with<br><em>their own story.</em></h2><p>Explore the photographs in the original Sandymount project gallery, including its separately named Westmeath examples.</p>'+link('/gallery-showroom/25/','View project photographs','button')+'</div>'+image('/assets/living.webp','Living space from the original Sandymount project gallery',507,640)+'</section>'
body+=gallery_collections
showroom=re.search(r'<section class="showroom section".*?</section>',home,re.S).group(0).replace('id="showroom"','id="visit"').replace('src="assets/','src="/assets/');body+=showroom+cta('An idea you <em>love?</em>','Visit Lucan Village to explore samples, fabrics and furnishings, or contact us to discuss your project.');page('Gallery & Showroom','Browse Weir Interiors’ showroom collections, fabrics, furniture and project photographs. Visit the Lucan Village showroom.','/gallery-showroom/',body)

# Individual gallery pages, retaining all imported photos.
for gid,(name,desc) in COLLECTIONS.items():
 photos=PHOTOS[gid];body=crumb(name,('/gallery-showroom/','Gallery & showroom'))+f'<section class="collection-intro section"><p class="eyebrow">WEIR INTERIORS · ORIGINAL COLLECTION</p><h1>{e(name)}</h1><p>{e(desc)}</p><span class="collection-count">{len(photos)} photographs · Select an image for a closer look</span></section>'
 body+='<section class="section photo-section" aria-label="'+e(name)+' photographs"><div class="photo-grid">'
 for i,p in enumerate(photos):
  if gid==25:
   f=p['original_filename'];alt='Westmeath project photograph' if 'Westmeath' in f else ('Sandymount project photograph' if 'Sandym' in f else 'Project photograph from the original gallery')
   if 'kitchen' in f.lower():alt+=' — bespoke kitchen'
   elif 'Living' in f:alt+=' — living area'
   elif 'balustrade' in f:alt+=' — balustrade and lighting'
   elif 'bathroom' in f:alt+=' — bathroom'
   elif 'Cloakroom' in f:alt+=' — cloakroom'
   elif 'sink' in f:alt+=' — sink and panelling'
  else:alt=f'{name} collection example {i+1}'
  label=alt if gid==25 else f'{name} · {i+1:02d}'
  body+=f'<figure><a class="photo-link" href="{p["file"]}" data-full="{p["file"]}" data-caption="{e(alt)}" aria-label="Enlarge {e(alt)}">{image(p["thumb"],alt,p["thumbWidth"],p["thumbHeight"])}<span class="photo-action" aria-hidden="true">View photograph</span></a><figcaption>{e(label)}</figcaption></figure>'
 body+='</div></section><dialog class="lightbox" aria-labelledby="lightbox-caption"><div class="lightbox-toolbar"><button type="button" data-gallery-prev aria-label="Previous image">Previous</button><span id="lightbox-count"></span><button type="button" data-gallery-next aria-label="Next image">Next</button><button type="button" data-gallery-close>Close</button></div><img id="lightbox-image" alt="" width="1280" height="1280"><p id="lightbox-caption"></p></dialog>'
 body+='<section class="section collection-bottom">'+link('/gallery-showroom/','Back to all collections')+link('/contact/?service='+('Interior%20design' if gid==25 else 'D%C3%A9cor%20%26%20fabrics'),'Enquire about this collection','button')+'</section>'
 body+=cta('Let’s find the right<br><em>details for your home.</em>','Tell us which collection or image caught your eye. Availability and prices are confirmed by the team.');page(name,desc,f'/gallery-showroom/{gid}/',body)

# Contact
body=crumb('Contact')+contact.replace('<section class="contact section"','<section class="contact section contact-page"').replace('<h2 id="contact-title">','<h1 id="contact-title">').replace('</em></h2>','</em></h1>').replace('<em>imagining?</em></h2>','<em>imagining?</em></h1>')
# Replace only the primary contact heading closing tag, regardless of text formatting.
body=body.replace('<em>imagining?</em></h2>','<em>imagining?</em></h1>')
body+='<section class="section contact-visit"><div><p class="eyebrow">THE LUCAN SHOWROOM</p><h2>Come and<br><em>be inspired.</em></h2><address>8 Main Street, Lucan Village<br>Dublin K78 T8P2<br>Beside Bank of Ireland</address><p>Explore fabrics, furnishings and samples. Call before visiting to check a suitable time.</p>'+link('https://goo.gl/maps/idVkmbw6Sb38dbwu8','Get directions','button')+'</div>'+image('/assets/showroom2.webp','Fabrics and furnishings in the Lucan showroom',768,768)+'</section>'
body+=textsection('YOUR LOCATION','Local roots.<br><em>Room to go further.</em>',["Weir Interiors serves Dublin, Kildare, Meath and Wicklow, with enquiries welcomed for larger projects elsewhere in Ireland.","When enquiring, include your area and the changes you have in mind. If you have a particular collection image in mind, mention its name and image number.","For a showroom visit, phone the team to discuss a suitable time. For a project enquiry, use the email helper above or contact us directly."])
page('Contact & Project Enquiries','Contact Weir Interiors at 8 Main Street, Lucan Village, Dublin. Call 01 601 0972 or email enquiries@weirinteriors.ie.','/contact/',body)

# Preview-specific privacy page: do not invent an official legal policy.
body=crumb('Privacy & this preview')+'<section class="section legal-page"><p class="eyebrow">INDEPENDENT DESIGN CONCEPT</p><h1>Privacy &<br><em>this preview.</em></h1><p class="lead">This page explains the enquiry helper in this concept. It does not replace Weir Interiors’ official privacy policy.</p><h2>Your enquiry</h2><p>The form prepares an email draft using the information you enter. The page does not submit the form to a backend, store your project details or send an email automatically. You choose whether to send the draft from your email app.</p><h2>Email and telephone links</h2><p>Email links open your chosen mail application; telephone links ask your device to call the published number. Your mail provider and telephone service handle those actions.</p><h2>Images and external links</h2><p>The photographs and logo come from the existing Weir Interiors website and are served as local concept assets. Social profiles, directions and the official website open external destinations, which have their own privacy practices.</p><h2>Analytics and preview access</h2><p>The site code does not add analytics scripts, advertising trackers or browser storage. The preview hosting service manages access and may process technical information separately from this page.</p><h2>The official business policy</h2><p>The business’s existing policy remains available on its official website. Before an official launch, the owner must approve policy wording that matches the final hosting, enquiry form and analytics setup.</p>'+link('https://www.weirinteriors.ie/privacy-policy','Read the official Weir Interiors privacy policy')+'<p class="legal-date">Concept prepared 7 October 2026.</p></section>'
page('Privacy & This Preview','How the independent Weir Interiors design concept handles email drafts, external links and preview access.','/privacy-policy/',body)

# A dedicated missing-page screen avoids silently treating broken URLs as the homepage.
page('Page Not Found','The requested concept page could not be found.','/404/', '<section class="section legal-page"><p class="eyebrow">PAGE NOT FOUND</p><h1>Let’s find<br><em>your way back.</em></h1><p>This address is not a page in the concept.</p>'+link('/','Back to home','button')+link('/gallery-showroom/','Explore the gallery')+'</section>')
(DIST/'404.html').write_text((DIST/'404/index.html').read_text())
shutil.rmtree(DIST/'404')
print(json.dumps({'pages':len(list(DIST.rglob('index.html'))),'gallery_pages':len(COLLECTIONS),'imported_photos':len([x for x in DATA if x['ok']])}))
