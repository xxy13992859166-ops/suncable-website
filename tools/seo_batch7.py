"""SEO batch 7 - three fixes requested together.

1. Rewrite the 13 remaining "fill-in-the-blank" blog pages.  They shared one
   template with the topic noun swapped (C(13,2)=78 of the 78 remaining
   high-similarity blog pairs).  Each gets its own body, grounded in facts
   already published on the site plus standard references.
2. Unify the temperature claim.  About 30 places called -40..+120 C an
   *operating* temperature; EN 50618 / IEC 62930 datasheets say -40..+90 C
   ambient with 120 C maximum conductor temperature.  Only operating-range
   wording is touched; 2,000 h / 120 C ageing-test claims are left alone.
3. Replace assets/inquiry-form.js with a version that does not lose leads
   silently when the relay is unreachable: it submits by fetch, and on any
   failure it shows the email + WhatsApp fallback instead of redirecting to
   thankyou.html.  Native POST remains for no-JS.

Idempotent: blog bodies carry <!-- b7 -->, temperature rewrites are
context-anchored, and the JS is compared before writing.
"""

import pathlib
import re

MARK = "<!-- b7 -->"
BLOGS = {}


def art(name, body):
    BLOGS[name] = body.strip()


art("blog-carport-solar-cable.html", """
        <h2>What makes a carport different from a rooftop</h2>
        <p>A solar carport is a structure with moving parts, traffic underneath, and water that has to go somewhere. The cable is not lying on a static roof: it runs through a frame that flexes in wind, next to a surface that reflects sun onto it from below, and often past an EV charger that adds an AC circuit to the same steel. Each of those changes the specification.</p>

        <h2>Route the cable where the structure does not move</h2>
        <p>Fix cable runs to the static frame, not across the joints that move. Where a run must cross a movement joint — canopy to support column, or a sliding section on a tracked carport — leave a service loop sized to the movement rather than pulling the cable straight. Water follows the cable, so every horizontal run needs a drip point below the entry gland.</p>
        <table>
          <thead>
            <tr><th>Location</th><th>Risk</th><th>Answer</th></tr>
          </thead>
          <tbody>
            <tr><td>Canopy underside</td><td>Reflected UV and radiated heat</td><td>XLPO PV cable, keep clear of hot steel</td></tr>
            <tr><td>Movement joints</td><td>Fatigue at the bend</td><td>Service loop, no clamp within 100 mm of the joint</td></tr>
            <tr><td>Column base</td><td>Standing water</td><td>Gland above the flood line, drip loop</td></tr>
            <tr><td>EV charger feed</td><td>Mixed DC and AC in one duct</td><td>Separate containment, AC cable to 450/750 V</td></tr>
          </tbody>
        </table>

        <h2>Drainage and the underside environment</h2>
        <p>The area under a carport is shaded, splash-wetted and often planted. Cable trays that fill with water in winter are common. Slope trays to a drain, avoid low points between supports, and do not use the tray as a route for anything that needs to stay dry. If the tray is perforated, check the perforations before installation — a blocked tray is a bath.</p>

        <h2>Voltage drop across a long canopy</h2>
        <p>A 40-bay carport is a long, narrow array. Strings at the far end can be 100 m or more from the inverter, and the DC drop adds up over both legs. Size on the loop length and the 1–2 % design target; on a canopy the extra step in cross-section usually costs less than the yield it protects.</p>

        <h2>Inspection and maintenance access</h2>
        <p>Carport arrays are usually cleaned and inspected from below or from a lift. Put connectors where they can be reached without dismantling the canopy, and label strings at both ends so a fault can be located from the ground.</p>
        <p>Cable for carports is normally PV1-F 2-core (0.6/1 kV, 1.0–6.0 mm²) or H1Z2Z2-K single core, both XLPO and rated −40 °C to +90 °C ambient. Send the canopy layout and run lengths for a quote on <a href="/suncable-website/solar-cable-request-quote.html">solar cable for carports</a>.</p>
""")

art("blog-floating-solar-cable.html", """
        <h2>Why floating PV is a different cable problem</h2>
        <p>On a floating array the cable spends part of its life in water and all of its life in motion. Pontoons rise and fall with level and wave, the array rotates slowly around its mooring, and the cable between floats is loaded every time the water moves. A cable that survives a rooftop for 25 years can fail in three seasons here if the mechanical design is wrong.</p>

        <h2>The cable is not the first decision — the route is</h2>
        <p>Decide where the cable is dry, where it is submerged, and where it is merely splashed, because each zone needs different hardware:</p>
        <ul>
          <li><strong>On the float</strong> — fixed to the pontoon frame, UV-exposed, splashed. Standard XLPO PV cable is appropriate, supported so it does not chafe on the frame edge.</li>
          <li><strong>Between floats</strong> — the moving section. This needs a service loop and a strain-relief, or the movement is transferred into the conductor.</li>
          <li><strong>Submerged run to shore</strong> — the length that must tolerate continuous immersion. Specify the construction and the depth with the supplier in writing; not every PV cable is offered for permanent immersion.</li>
        </ul>

        <h2>Water ingress happens at the joint, not in the cable</h2>
        <p>Immersion does not usually damage a sound cable; it finds the terminations. Three rules that prevent most floating-PV moisture failures:</p>
        <table>
          <thead>
            <tr><th>Rule</th><th>Why</th></tr>
          </thead>
          <tbody>
            <tr><td>Terminate above the waterline</td><td>Joints are the weak point; keep them dry and reachable</td></tr>
            <tr><td>Gland matched to cable OD</td><td>An IP68 connector with an oversized gland still leaks</td></tr>
            <tr><td>Strain relief both sides of a joint</td><td>Movement must not arrive at the contact</td></tr>
          </tbody>
        </table>

        <h2>UV where the cable leaves the water</h2>
        <p>The shore transition is the harshest metre on the site: wet, sunlit, walked on, and often where the cable bends. Protect it in conduit, keep the bend radius generous, and record the route so a later dredging or anchoring operation does not cut it.</p>

        <h2>Inspection that actually finds problems</h2>
        <p>Insulation resistance to earth, measured per string at commissioning and again after the first wet season, is the cheapest early warning available. A string whose reading drifts downward is where water is getting in.</p>
        <p>For floating projects we quote PV1-F and H1Z2Z2-K with TÜV and UL documentation and discuss the submerged section construction case by case. Send the layout and the depth to <a href="/suncable-website/solar-cable-request-quote.html">request a quotation</a>.</p>
""")

art("blog-solar-cable-2027-preview.html", """
        <h2>Three changes worth planning for now</h2>
        <p>Nobody can forecast a cable price a year out, and this page will not pretend to. What can be said with confidence is that three technical directions are already visible in tenders, and each changes what a buyer should specify. They are worth planning for because they change drawings, not because they change headlines.</p>

        <h2>1. Higher DC system voltages</h2>
        <p>1500 V DC systems are now ordinary on utility-scale work, and the cable and connector on the DC side must both be rated for it. The mistake to avoid is a 1500 V connector on a 1000 V cable, or the reverse — the system is only as rated as its weakest link. When you write a specification, state the system voltage and require the certificate to cover it.</p>

        <h2>2. Storage coupled on the DC side</h2>
        <p>More projects now put batteries behind the same DC bus as the array. That adds a cable duty the PV side never had: high continuous current at low voltage, in an enclosure, often indoors. It is a different product from PV cable — low-smoke halogen-free construction, sized for current rather than voltage drop — and it should be a separate line on the bill of materials.</p>

        <table>
          <thead>
            <tr><th>Direction</th><th>What it changes in your specification</th></tr>
          </thead>
          <tbody>
            <tr><td>1500 V DC</td><td>Cable and connector rated and certified at 1500 V, not just the inverter</td></tr>
            <tr><td>DC-coupled storage</td><td>Separate LSZH battery cable, sized on current</td></tr>
            <tr><td>Traceability</td><td>Batch test certificate per drum, production address on the certificate</td></tr>
          </tbody>
        </table>

        <h2>3. Traceability from certificate to drum</h2>
        <p>Inspection regimes are asking a question that used to be answered with a logo: which factory made this drum, and does the certificate name it? The practical preparation is unglamorous — keep the certificate scope by size, the batch test report, and the production address together, and make sure they refer to the same entity. Suppliers who cannot produce that set will increasingly be filtered out at tender stage, not at delivery.</p>

        <h2>What does not change</h2>
        <p>The fundamentals stay: XLPO insulation, tinned copper Class 5 conductor, a certificate that covers the size you are buying, and a joint made with the right tool. Any specification that sacrifices those for a new feature is trading a certain benefit for an uncertain one.</p>
        <p>If you are writing a 2027 specification now, send us the draft cable schedule and we will tell you which line items our documentation covers at <a href="/suncable-website/solar-cable-request-quote.html">the quotation page</a>.</p>
""")

art("blog-solar-cable-agriculture.html", """
        <h2>Three agricultural loads, three different cables</h2>
        <p>Farm solar is not one application. A barn roof, an irrigation pump and a livestock building put the cable in three different environments, and a specification written for one of them is usually wrong for the other two. This page covers the building and pump side; field-scale agrivoltaics is covered separately.</p>

        <h2>Barn and shed roofs</h2>
        <p>Corrugated roof, dust, birds, and a structure that was never designed to carry cable. The practical issues are mechanical: fixings that do not pierce the sheet, cable kept off the roof surface so water can drain, and a route that a person can inspect without walking the panels. Where the run drops down a wall, protect it in conduit to the first disconnect — that is where machinery catches it.</p>

        <h2>Irrigation pumps and boreholes</h2>
        <p>Pump installations combine a long cable run with a wet environment and, often, a variable-frequency drive. Two points decide whether the installation behaves:</p>
        <ul>
          <li><strong>Voltage drop over the run to the pump.</strong> A borehole 200 m from the panel is a 400 m loop. Size on the loop and keep the drop inside the drive's input tolerance.</li>
          <li><strong>VFD harmonics and cable length.</strong> Long motor cables from a drive need the drive manufacturer's cable guidance — shielded construction and length limits are a drive requirement, not a PV cable question.</li>
        </ul>

        <h2>Livestock buildings</h2>
        <p>Ammonia, dust, rodents and washdown. Cable in poultry or dairy housing should be in conduit, fixed off ledges where dust collects, and specified with a halogen-free XLPO construction rather than PVC, which embrittles faster under chemical and thermal load. Keep connectors out of reach of animals and above washdown level.</p>

        <table>
          <thead>
            <tr><th>Load</th><th>Dominant risk</th><th>Practical answer</th></tr>
          </thead>
          <tbody>
            <tr><td>Barn roof array</td><td>Mechanical, water shedding</td><td>Off-surface routing, wall conduit to disconnect</td></tr>
            <tr><td>Irrigation pump</td><td>Voltage drop, wet ground</td><td>Size on loop length, follow VFD cable guidance</td></tr>
            <tr><td>Livestock building</td><td>Ammonia, rodents, washdown</td><td>Conduit, XLPO not PVC, connectors out of reach</td></tr>
          </tbody>
        </table>

        <h2>One specification note that saves money</h2>
        <p>Do not use the array cable for the pump feed. They have different duties, different sizes and, in the case of a VFD, different screening requirements. Splitting them on the bill of materials makes the quotation comparable and the installation inspectable.</p>
        <p>PV1-F 2-core and H1Z2Z2-K single core cover the array side, with the 450/750 V 3-core for the AC pump feed. Send the loads and run lengths to <a href="/suncable-website/solar-cable-request-quote.html">get a quotation</a>.</p>
""")

art("blog-solar-cable-bidding.html", """
        <h2>Tenders are lost on documents, not on price</h2>
        <p>On an international tender the cable package is small and the paperwork is not. Most disqualifications we see are technical: a certificate that does not cover the size tendered, a test report in the wrong language, a datasheet that contradicts the certificate, or a bid that responds to a different standard than the one specified. All of them are avoidable before submission.</p>

        <h2>The document set that survives review</h2>
        <ul>
          <li><strong>Certificate with scope by size.</strong> Not the cover page — the schedule showing which cross-sections are covered.</li>
          <li><strong>Type-test report</strong> for thermal endurance, cold bend and UV, with the laboratory named.</li>
          <li><strong>Batch test certificate</strong> for the production run, if the tender asks for pre-delivery evidence.</li>
          <li><strong>Datasheet matching the certificate</strong> — same standard, same temperature class, same conductor class.</li>
          <li><strong>Declaration of conformity</strong> and, where required, the material declarations for the insulation.</li>
        </ul>

        <h2>Read the technical specification before pricing</h2>
        <table>
          <thead>
            <tr><th>Clause to check</th><th>Why bids fail on it</th></tr>
          </thead>
          <tbody>
            <tr><td>Standard reference</td><td>Quoting IEC 62930 where EN 50618 is specified (or the reverse)</td></tr>
            <tr><td>Temperature class</td><td>Offering −40/+90 when the spec asks for a stated maximum conductor temperature</td></tr>
            <tr><td>Conductor class</td><td>Class 5 required, Class 2 offered</td></tr>
            <tr><td>Test evidence</td><td>Type test offered where batch test is required</td></tr>
            <tr><td>Delivery terms</td><td>CIF priced where the schedule is FOB port of loading</td></tr>
          </tbody>
        </table>

        <h2>Price the scope, not the cable</h2>
        <p>A tender is usually won or lost on the landed cost of the package. Build the price from the same four blocks every time: cable by size, drums and packing, freight and insurance to the stated Incoterm, and the documentation and testing the tender demands. Two bids that differ by a few percent per metre are usually differing on drum returns or on who pays for the pre-shipment inspection.</p>

        <h2>Lead time is a bid qualification</h2>
        <p>State the lead time you can hold, and what could change it. A 7–15 day standard lead time with a clear statement of what pushes it out is more persuasive to an evaluator than an optimistic date that slips after award — the second one turns into a claim.</p>

        <h2>What we provide for tenders</h2>
        <p>Certificate scope by size, type-test references, batch certificates and datasheets for PV1-F, H1Z2Z2-K, MC4 connectors, storage and AC cable, in English. Send the tender's cable schedule and the technical clauses to <a href="/suncable-website/solar-cable-request-quote.html">our quotation desk</a> and we will come back with a compliant offer or an explicit list of deviations.</p>
""")

art("blog-solar-cable-case-study-africa.html", """
        <h2>What southern African sites demand from cable</h2>
        <p>We are not going to publish a project case study with figures we cannot substantiate. What we can describe honestly is the specification pattern that southern African projects keep arriving at, because the environment drives it: high irradiance, high ambient temperature, dust, and — in coastal installations — salt.</p>

        <h2>Heat is a derating problem before it is a cable problem</h2>
        <p>An ambient of 40 °C at the site is not the temperature in a roof void or inside a combiner enclosure, which can run 15–20 K higher. Two consequences follow: the current-carrying capacity used in the design must be derated for the real enclosure temperature, and the cable's temperature class has to be read correctly — −40 °C to +90 °C ambient operation, with 120 °C as the maximum conductor temperature, not a working ambient.</p>

        <h2>UV, dust and cleaning cycles</h2>
        <ul>
          <li><strong>UV:</strong> XLPO insulation to IEC 62930 or EN 50618 is the baseline; PVC-jacketed "solar" cable does not survive the exposure.</li>
          <li><strong>Dust:</strong> accumulates on trays and in connectors; plan cleaning access and do not rely on rain to clear a horizontal run.</li>
          <li><strong>Cleaning:</strong> water and brushes at pressure are a mechanical load on cable and connectors — specify glands and supports that tolerate it.</li>
        </ul>

        <h2>Coastal and industrial salt</h2>
        <p>Within a few kilometres of the coast, the failure mode shifts to corrosion at terminations. The mitigation is not a different cable so much as better joints: IP68 connectors seated on the correct gland, contacts inspected at the first annual service, and no bare copper left exposed. In industrial and mining environments the same applies with sulphur and dust added.</p>

        <table>
          <thead>
            <tr><th>Site condition</th><th>Specification response</th></tr>
          </thead>
          <tbody>
            <tr><td>High ambient and hot enclosures</td><td>Derate for enclosure temperature; confirm temperature class wording</td></tr>
            <tr><td>High UV</td><td>XLPO to IEC 62930 / EN 50618</td></tr>
            <tr><td>Coastal salt</td><td>IP68 joints, correct gland, annual contact inspection</td></tr>
            <tr><td>Dust and cleaning</td><td>Accessible routing, connectors above washdown level</td></tr>
          </tbody>
        </table>

        <h2>Compliance paperwork in the region</h2>
        <p>South African projects typically ask for SABS-related evidence; Nigerian projects for SONCAP; Gulf projects for SASO or equivalent. Those are market-access requirements layered on top of the product certificate, not substitutes for it. Our <a href="/suncable-website/export-markets.html">export markets page</a> sets out which certificate applies where.</p>
        <p>For a project-specific offer, send the cable schedule and destination port to <a href="/suncable-website/solar-cable-request-quote.html">the quotation page</a>.</p>
""")

art("blog-solar-cable-for-residential.html", """
        <h2>Residential is where oversizing is cheapest</h2>
        <p>A home array is small, the run from roof to inverter is short, and the cable is a trivial share of the installed cost. That combination makes it the one place where choosing a size up, and choosing a certified cable, costs almost nothing — and where the cost of getting it wrong lands on a homeowner rather than a maintenance budget.</p>

        <h2>Sizing in three steps</h2>
        <ol>
          <li><strong>String current.</strong> Take the module's short-circuit current and apply the relevant multiplier from the installation standard for the local condition.</li>
          <li><strong>Voltage drop.</strong> Use the loop length — up the roof, across, and back down. Keep the DC drop inside the 1–2 % design target; on a 20 m loop this is rarely the constraint, on a detached garage it often is.</li>
          <li><strong>Ambient correction.</strong> Cable in a loft or behind a roof tile runs hotter than the outside air temperature on the datasheet.</li>
        </ol>

        <h2>What to insist on, even on a small job</h2>
        <table>
          <thead>
            <tr><th>Item</th><th>Why it matters at home</th></tr>
          </thead>
          <tbody>
            <tr><td>XLPO PV cable, not PVC "solar" cable</td><td>UV and heat performance over 25 years</td></tr>
            <tr><td>Tinned copper Class 5 conductor</td><td>Corrosion resistance and flexibility at tight bends</td></tr>
            <tr><td>IP68 connectors, one brand per string</td><td>Most residential callbacks are joint failures</td></tr>
            <tr><td>Documented certification</td><td>Warranty and insurance questions later</td></tr>
          </tbody>
        </table>

        <h2>Battery additions and the second run</h2>
        <p>If a battery is likely within a few years, leave capacity in the route now: a spare duct from roof to plant room costs a fraction of re-opening a finished wall. The battery itself needs a different cable — low-smoke halogen-free DC cable sized on current, not on voltage drop — so plan it as a second circuit rather than re-using the PV run.</p>

        <h2>Beware the kit cable</h2>
        <p>Many small systems ship with pre-terminated cable of unknown origin. It is often the weakest part of an otherwise sound install. If you cannot identify the standard the cable was made to, replace it — the cost is small and the alternative is discovering the problem in year six.</p>
        <p>We supply PV1-F 2-core (0.6/1 kV, 1.0–6.0 mm²) and H1Z2Z2-K single core in small quantities with the same certification as our project orders. Send your string layout to <a href="/suncable-website/solar-cable-request-quote.html">get a quote</a>.</p>
""")

art("blog-solar-cable-japan.html", """
        <h2>Three Japanese conditions that change the cable specification</h2>
        <p>Japanese installations combine seismic movement, typhoon wind loading and — on a large share of the population's coastline — salt air. None of these is exotic on its own; together they put more mechanical and chemical demand on the DC side than a European rooftop does.</p>

        <h2>Seismic movement: plan for displacement, not for load</h2>
        <p>Racking is designed to move without failing. Cable should be designed the same way: fixed to the structure, but with service loops where two parts of the structure can displace relative to each other. The failure signature is a conductor broken inside intact insulation, at a clamp that was too tight near a joint.</p>

        <h2>Typhoon wind loading</h2>
        <ul>
          <li>Support spacing closer than on a sheltered site — a cable that whips against an edge for a decade will chafe through.</li>
          <li>No connectors left hanging on the cable; strain-relieve at the rail.</li>
          <li>Route in conduit where the run is exposed on the windward edge.</li>
        </ul>

        <h2>Salt air on coastal sites</h2>
        <p>Corrosion starts at terminations and at any nick in the jacket. IP68 connectors with the gland matched to the cable, annual inspection of contacts at the first service, and a cable with a tinned copper conductor are the practical measures. Untinned copper in a salt environment is a maintenance liability regardless of how good the insulation is.</p>

        <table>
          <thead>
            <tr><th>Condition</th><th>Design response</th></tr>
          </thead>
          <tbody>
            <tr><td>Seismic displacement</td><td>Service loops at joints, clamps clear of bends</td></tr>
            <tr><td>Typhoon wind</td><td>Closer supports, strain relief, conduit on exposed edges</td></tr>
            <tr><td>Salt air</td><td>Tinned conductor, IP68 joints, annual contact check</td></tr>
            <tr><td>Documentation</td><td>IEC 62930 / EN 50618 evidence, translated if the specification requires it</td></tr>
          </tbody>
        </table>

        <h2>Documentation expectations</h2>
        <p>Japanese buyers usually accept IEC-based evidence with a clear certificate scope, and increasingly ask for traceability between the certificate holder and the producing factory. If a JIS-aligned document set is specified, that is a buyer requirement we will confirm case by case rather than assume.</p>
        <p>PV1-F and H1Z2Z2-K are supplied with TÜV, UL and CE documentation; state the port and the sizes and we will quote through <a href="/suncable-website/solar-cable-request-quote.html">the quotation page</a>, and say plainly if a document you need is outside our scope.</p>
""")

art("blog-solar-cable-odm-oem.html", """
        <h2>What private label actually changes</h2>
        <p>ODM and OEM mean different things in this trade and are often used interchangeably. OEM is your specification, your marking, our production. ODM is our design and specification, your brand. The distinction decides who owns the certificate, who carries the liability if the cable fails, and whether the marking on the drum can legally appear at all.</p>

        <h2>The certificate question comes first</h2>
        <p>A certificate belongs to a named holder for a defined product. Putting your brand on a drum does not transfer it. Three arrangements exist, and they are not equivalent:</p>
        <ul>
          <li><strong>Relabelling.</strong> The cable is certified under the factory's name; your brand appears on the drum and the delivery documents. Cheapest, but the certificate never names you.</li>
          <li><strong>Certificate extension.</strong> Your brand is added to the existing certificate as a licensed mark, with the certificate body's agreement. Requires paperwork and time.</li>
          <li><strong>Own certification.</strong> The product is certified under your name. Slowest and most expensive, but the only version that survives a tender asking whose certificate it is.</li>
        </ul>

        <h2>Marking, packaging and the details buyers forget</h2>
        <table>
          <thead>
            <tr><th>Item</th><th>Decide before the order</th></tr>
          </thead>
          <tbody>
            <tr><td>Print legend</td><td>Brand, standard, size, metre marking — and who approves the artwork</td></tr>
            <tr><td>Drum label</td><td>Brand, batch, length, production date, handling marks</td></tr>
            <tr><td>Documents</td><td>Datasheet, certificate reference, packing list under your name</td></tr>
            <tr><td>Colour</td><td>Standard red/black or a custom colour, with the MOQ that implies</td></tr>
          </tbody>
        </table>

        <h2>MOQ and the economics of a private label run</h2>
        <p>Private label adds setup cost: artwork, print cylinder or ink jet programming, drum labels, and a separate batch record. That cost is spread over the run, so the realistic question is not "what is the MOQ" but "what run makes the setup negligible". Our standard MOQ is 1 km per colour; a private label run needs more than that to be worth doing for both sides, and we will say so rather than take an order that loses money on both sides.</p>

        <h2>What we need from you</h2>
        <p>Brand artwork, the specification you want produced, the sizes and the annual volume you expect. We will come back with the production basis, the certification arrangement that fits it, and a lead time. Start at <a href="/suncable-website/solar-cable-request-quote.html">the quotation page</a>.</p>
""")

art("blog-solar-cable-planning.html", """
        <h2>Cable is ordered late and needed early</h2>
        <p>On most projects the cable package is released after the modules and the inverter are fixed, which puts it at the end of the procurement queue and the start of the installation sequence. That mismatch is where programme risk lives. Planning the cable from the construction schedule backwards, rather than from the bill of materials forwards, is the fix.</p>

        <h2>Build the budget from four blocks</h2>
        <table>
          <thead>
            <tr><th>Block</th><th>What it contains</th><th>Where it goes wrong</th></tr>
          </thead>
          <tbody>
            <tr><td>Cable by size</td><td>Metres per cross-section, not a single blended figure</td><td>Blended prices hide the size mix</td></tr>
            <tr><td>Drums and packing</td><td>Drum lengths, returnable or one-way, pallets</td><td>Return freight forgotten</td></tr>
            <tr><td>Freight and insurance</td><td>To the stated Incoterm and port</td><td>CIF quoted, FOB specified</td></tr>
            <tr><td>Testing and documents</td><td>Batch certificates, third-party inspection</td><td>Added after award</td></tr>
          </tbody>
        </table>

        <h2>Decide drum lengths with the electrician, not the buyer</h2>
        <p>Drum length is the single most under-planned variable. Too short and you add joints in the field; too long and you carry an offcut and a heavier drum around site. Get the run list before the order is placed and match drums to runs — this is the one part of the purchase where a supplier can genuinely save the customer money rather than shift margin.</p>

        <h2>Phase the delivery, not just the order</h2>
        <ul>
          <li><strong>First delivery:</strong> the sizes needed for the first week of DC work, so installation starts on time.</li>
          <li><strong>Second delivery:</strong> the balance, timed to storage capacity on site.</li>
          <li><strong>Buffer:</strong> a small allowance of the most-used size for termination losses and site damage — cheaper than an air freight for 200 m.</li>
        </ul>

        <h2>Price risk belongs in the contract, not in the estimate</h2>
        <p>Copper moves and freight moves. A quotation that states its copper base date lets you see what changed if the order is placed weeks later; a quotation that does not leaves the adjustment to be discovered at invoice. Ask for the base date in writing, and agree in the purchase order what happens if it moves before shipment.</p>

        <h2>Plan the documentation with the delivery</h2>
        <p>Certificates, batch test records and packing lists should be scheduled as deliverables with dates, not requested at handover. If the consultant specified a document set, confirm it at order placement — amending a certificate after the drums are on site is the slowest link in any closeout.</p>
        <p>Send the run list and the delivery phasing to <a href="/suncable-website/solar-cable-request-quote.html">our quotation desk</a>; standard lead time is 7–15 days and MOQ is 1 km per colour.</p>
""")

art("blog-solar-cable-retrofit.html", """
        <h2>Replace the cable, or the whole DC side?</h2>
        <p>On a retrofit the cable is rarely the only degraded component. Connectors, string fuses and sometimes the modules themselves are at end of life too. Deciding what to keep is an economics question with a safety floor: anything that cannot be shown to be sound should not be re-energised.</p>

        <h2>When replacement is not optional</h2>
        <ul>
          <li><strong>Jacket cracking or chalking</strong> along a run — the compound has aged out, and the conductor underneath is no longer protected.</li>
          <li><strong>Insulation resistance to earth</strong> that has fallen below the value recorded at commissioning and continues to fall.</li>
          <li><strong>PVC or unknown-origin cable</strong> on a DC array, whatever it looks like.</li>
          <li><strong>Undersized runs</strong> that were marginal at commissioning and are now carrying more current after an array expansion.</li>
          <li><strong>Any cable that has been wet internally</strong> — water travels along strands and corrosion continues after the visible damage is gone.</li>
        </ul>

        <h2>The safe sequence</h2>
        <ol>
          <li>Isolate and lock off, and treat the DC side as live until proven otherwise — a string in daylight is a source, not a load.</li>
          <li>Measure and record insulation resistance per string before disturbing anything; that baseline is what proves the new installation is better.</li>
          <li>Remove and label; photograph the routing before it is dismantled.</li>
          <li>Replace connectors as well as cable where the connector age is unknown — a new cable on an old joint moves the failure point, it does not remove it.</li>
          <li>Re-test per string and compare with the pre-works record.</li>
        </ol>

        <h2>Partial replacement traps</h2>
        <p>Replacing one string run and leaving its neighbours is common and usually fine, provided the new cable matches the old in size and construction. Mixing sizes on parallel strings creates unequal current sharing, and mixing old PVC with new XLPO creates two different ageing rates on the same array. Match, or replace the set.</p>

        <table>
          <thead>
            <tr><th>Situation</th><th>Decision</th></tr>
          </thead>
          <tbody>
            <tr><td>Cracked jacket on one run</td><td>Replace the run; inspect adjacent runs</td></tr>
            <tr><td>Falling insulation resistance</td><td>Investigate joints first, then replace</td></tr>
            <tr><td>Array expanded, runs marginal</td><td>Re-size on the new current</td></tr>
            <tr><td>Unknown-origin cable</td><td>Replace regardless of appearance</td></tr>
          </tbody>
        </table>

        <h2>Documenting the retrofit</h2>
        <p>Record the cable type, size, batch and test results for the replaced sections. A retrofit without that record becomes an unknown-origin installation the next time someone inspects it — which is where the cycle starts again.</p>
        <p>For replacement quantities, send the run list and string count to <a href="/suncable-website/solar-cable-request-quote.html">the quotation page</a>; PV1-F and H1Z2Z2-K are available with the documentation an inspector will ask for.</p>
""")

art("blog-solar-cable-storage.html", """
        <h2>Battery cable is a current problem</h2>
        <p>The PV side is designed around voltage and voltage drop. The battery side is designed around current: hundreds of amps at low voltage, in a confined space, next to equipment that must not be exposed to smoke. That is why the correct product is not PV cable with a different label, but a low-smoke halogen-free DC cable sized on current.</p>

        <h2>Sizing the battery-to-inverter run</h2>
        <ul>
          <li><strong>Current first.</strong> Take the inverter's maximum DC current, add the margin the manufacturer specifies, then check the cable against the ambient inside the enclosure — not the room.</li>
          <li><strong>Short-circuit withstand.</strong> A battery can deliver fault current far above its rating. The protective device and the cable have to be coordinated so the device clears the fault before the cable is damaged.</li>
          <li><strong>Equal links in parallel banks.</strong> Every parallel string should have the same cable length and cross-section, or the strings will not share current evenly.</li>
        </ul>

        <h2>Why low smoke, and where it matters</h2>
        <table>
          <thead>
            <tr><th>Location</th><th>Construction</th><th>Reason</th></tr>
          </thead>
          <tbody>
            <tr><td>Battery room / container</td><td>LSZH DC cable, 0.6/1 kV</td><td>Smoke and halogen emission in an occupied or enclosed space</td></tr>
            <tr><td>Indoor cabinet to inverter</td><td>LSZH DC cable</td><td>Confined route, high current</td></tr>
            <tr><td>Outdoor DC between cabinets</td><td>PV or DC cable per the enclosure rating</td><td>UV and water rather than smoke</td></tr>
          </tbody>
        </table>

        <h2>Routing in confined spaces</h2>
        <p>Battery containers are tight, hot, and packed with equipment. Three practical rules: keep the DC power cables physically separated from communication and sensing leads, respect the bend radius at the tightest corner in the enclosure rather than at the drum, and leave enough slack at the terminals for a re-termination without re-pulling the run.</p>

        <h2>Commissioning checks worth doing</h2>
        <p>Torque every terminal and mark it, measure insulation resistance before energising, and record the readings by circuit. Then measure contact temperature under load at the first opportunity: a termination that runs noticeably warmer than its neighbours is the one that will fail, and it will fail at the worst time for the site.</p>

        <h2>What we supply</h2>
        <p>Storage battery DC cable: LSZH, 0.6/1 kV, TÜV certified, with matching lugs and the documentation the enclosure inspector asks for. Send the inverter model, bank voltage and run lengths to <a href="/suncable-website/solar-cable-request-quote.html">the quotation page</a>.</p>
""")

art("blog-solar-cable-year-review.html", """
        <h2>The six questions we were asked most in 2026</h2>
        <p>This is not a market report with numbers we cannot substantiate. It is a summary of what buyers actually asked us across the year, and the short answer to each — the questions repeat because the same three or four decisions decide most purchases.</p>

        <h2>1. "Is this certificate real?"</h2>
        <p>Take the number and check it on the issuing body's own database — Certipedia for TÜV Rheinland, Product iQ for UL. Then read the scope line: a certificate for 4 mm² does not cover 6 mm². Most doubts end there.</p>

        <h2>2. "Can you meet this price?"</h2>
        <p>Usually the comparison is not like for like. FOB against CIF, a different size mix, a different drum length, or a certificate scope that is narrower than the one specified. Compare per size, per drum, delivered to the same port.</p>

        <h2>3. "What is your MOQ?"</h2>
        <p>1 km per colour on standard sizes. Below that the setup cost dominates, and a supplier who accepts it is either losing money or substituting material.</p>

        <h2>4. "How fast can you ship?"</h2>
        <p>7–15 days for standard specifications. What moves it: non-standard colours, private label printing, and third-party inspection. Ask which of those apply rather than asking for an earlier date.</p>

        <h2>5. "Why is 120 °C in your datasheet if the standard says 90 °C?"</h2>
        <p>Because they are two different numbers. −40 °C to +90 °C is the ambient operating range; 120 °C is the maximum conductor temperature, qualified by long-duration ageing testing. Any datasheet that presents 120 °C as an ambient operating range is misreading its own certification.</p>

        <table>
          <thead>
            <tr><th>Question</th><th>Where the answer lives</th></tr>
          </thead>
          <tbody>
            <tr><td>Certificate authenticity</td><td><a href="/suncable-website/solar-cable-certification-guide.html">Certification guide</a></td></tr>
            <tr><td>Price comparability</td><td><a href="/suncable-website/blog-solar-cable-price-trend-2026.html">Price trends</a></td></tr>
            <tr><td>Supplier vetting</td><td><a href="/suncable-website/how-to-verify-solar-cable-supplier-quality.html">Verification guide</a></td></tr>
            <tr><td>Installation faults</td><td><a href="/suncable-website/blog-solar-cable-fault-diagnosis.html">Fault diagnosis</a></td></tr>
          </tbody>
        </table>

        <h2>6. "Who honours the warranty?"</h2>
        <p>The entity that issues it, in the country where the claim is made. A 25-year claim from a company that re-labels drums is a promise without a factory. Ask for the certificate holder's name and check it matches.</p>

        <h2>What stays constant</h2>
        <p>Across every market we shipped to this year, the purchases that went well had the same shape: a stated specification, a certificate that matched it, a sample before the bulk order, and a drum plan agreed before production. None of that is new, which is why it keeps working.</p>
        <p>If your question is not on the list, send it. We answer specification questions at <a href="/suncable-website/solar-cable-request-quote.html">the quotation page</a> or on WhatsApp.</p>
""")

# --------------------------------------------------------------------------
# Titles that no longer match what the page can honestly deliver
# --------------------------------------------------------------------------
TITLES = {
    "blog-solar-cable-case-study-africa.html": (
        "Solar Cable for South Africa: Heat, UV and SABS",
        "Solar Cable for Southern Africa: Heat, UV and Compliance",
        "Specification guide for southern African PV projects: derating for "
        "enclosure heat, UV exposure, coastal salt and the compliance route.",
    ),
    "blog-solar-cable-year-review.html": (
        "Solar Cable: 6 Questions Buyers Asked Most in 2026",
        "Solar Cable: The Six Questions Buyers Asked Most in 2026",
        "The six questions we were asked most often this year: certificate "
        "authenticity, price comparability, MOQ, lead time, temperature class.",
    ),
    "blog-solar-cable-agriculture.html": (
        "Agricultural Solar Cable: Barns, Pumps, Livestock",
        "Agricultural Solar Cable: Barns, Pumps and Livestock Buildings",
        "Cable selection for farm buildings, irrigation pumps and livestock "
        "housing: ammonia, washdown, VFD runs and voltage drop over long loops.",
    ),
}

BLOG_ANCHOR = re.compile(
    r"(?is)<h2>\s*Introduction\s*</h2>.*?(?=</div>\s*<div\s+class=\"sidebar\">)")

# --------------------------------------------------------------------------
# Temperature wording: -40..+120 C as an operating range -> +90 C
# --------------------------------------------------------------------------
TEMP_RE = re.compile(r"(-40\s*(?:°\s*C|C)?\s*(?:to|~)\s*)\+?\s*(120)(\s*°?\s*C)")
TEMP_EXCL = ("max", "maximum", "conductor", "test", "aging", "ageing",
             "cycling", "withstand", "short-circuit", "short circuit")

TEMP_SPECIAL = [
    ("PV1-F is rated -40°C to +120°C, H1Z2Z2-K is -40°C to +90°C",
     "Both PV1-F and H1Z2Z2-K are rated -40°C to +90°C ambient, with a 120°C maximum conductor temperature"),
    ("TUV certified for extreme desert temperatures up to 120°C",
     "TUV certified for extreme desert conditions, with a -40°C to +90°C ambient rating"),
    ("PV cables are rated for -40°C to +120°C continuous operation, with short-circuit tolerance up to 250°C",
     "PV cables are rated for -40°C to +90°C ambient in continuous operation, with a 120°C maximum conductor temperature and short-circuit tolerance up to 250°C"),
    ("Temperature range: -40°C to +120°C.",
     "Temperature range: -40°C to +90°C ambient (120°C maximum conductor temperature)."),
    ("temperature range -40°C to +90°C (H1Z2Z2-K) or +120°C (PV1-F)",
     "temperature range -40°C to +90°C ambient for both PV1-F and H1Z2Z2-K, with a 120°C maximum conductor temperature"),
]

# IEC 62541 is OPC UA (industrial communication), not a cable standard.
# PV cable is IEC 62930; the H1Z2Z2-K designation comes from EN 50618.
STD_RE = re.compile(r"IEC\s*62541", re.I)
STD_ENC = re.compile(r"IEC%2062541", re.I)

# Exact strings where the generic rule cannot infer which standard is meant.
STD_EXACT = [
    ("Solar Cable Standards: IEC 62930, 62541 & UL 4703",
     "PV Cable Standards: IEC 62930, EN 50618 & UL 4703"),
    ("IEC 62930, IEC 62541, UL 4703", "IEC 62930, EN 50618, UL 4703"),
    ("IEC 62541 defines requirements for single-core PV cables",
     "EN 50618 defines requirements for single-core PV cables"),
    ("IEC 62541: H1Z2Z2-K Standard", "EN 50618: H1Z2Z2-K Standard"),
    ("iec 62930, iec 62541", "iec 62930, en 50618"),
]


def fix_std(s):
    hits = []
    for a, b in STD_EXACT:
        if a in s:
            n = s.count(a)
            s = s.replace(a, b)
            hits.extend([b] * n)
    s, n_enc = STD_ENC.subn("IEC%2062930", s)
    hits.extend(["IEC%2062930"] * n_enc)

    def sub(m):
        after = s[m.end():m.end() + 30]
        before = s[max(0, m.start() - 30):m.start()]
        if ("H1Z2Z2-K" in after and "PV1-F" not in after) or \
           ("H1Z2Z2-K" in before and "PV1-F" not in before):
            rep = "EN 50618"
        else:
            rep = "IEC 62930"
        hits.append(rep)
        return rep

    return STD_RE.sub(sub, s), hits

JS_PATH = "assets/inquiry-form.js"

NEW_JS = r"""/* Inquiry form v2 - resilient submit.
   Posts by fetch; if the relay is unreachable or rejects the submission the
   visitor gets a prefilled email and WhatsApp fallback instead of a fake
   thankyou page. Native POST still works without JS. */
(function () {
  if (window.__jlccInquiryFormLoaded) { return; }
  window.__jlccInquiryFormLoaded = true;

  var EMAIL = 'xxy13992859166@gmail.com';
  var ACTION = 'https://formsubmit.co/' + EMAIL;
  var AJAX = 'https://formsubmit.co/ajax/' + EMAIL;
  var WA = 'https://wa.me/8615339005193';
  var NEXT = 'https://xxy13992859166-ops.github.io/suncable-website/thankyou.html';

  function field(form, n) {
    var el = form.querySelector('[name="' + n + '"]');
    return el ? String(el.value || '') : '';
  }

  function showFallback(form, why) {
    var name = field(form, 'name'), company = field(form, 'company');
    var email = field(form, 'email'), phone = field(form, 'phone');
    var msg = field(form, 'message');
    var subject = 'Solar cable inquiry - ' + (company || name || 'website');
    var body = 'Name: ' + name + '\nCompany: ' + company + '\nEmail: ' + email +
      '\nPhone: ' + phone + '\n\n' + msg + '\n\nSent from: ' + location.href;
    var mail = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(body);
    var wa = WA + '?text=' + encodeURIComponent('Inquiry from ' + location.pathname + '\n' + body);

    var old = document.getElementById('jlcc-fallback');
    if (old) { old.parentNode.removeChild(old); }
    var box = document.createElement('div');
    box.id = 'jlcc-fallback';
    box.setAttribute('style', 'margin-top:14px;padding:14px 16px;border-radius:8px;background:#fff7ed;border:1px solid #f0b46b;color:#7a4a10;font-size:14px;line-height:1.55');
    box.innerHTML = '<strong>Our form relay did not respond.</strong><br>' +
      'Your details are still in the form. Send them directly and we will reply the same way:' +
      '<div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap">' +
      '<a href="' + mail + '" style="padding:9px 14px;border-radius:6px;background:#2563eb;color:#fff;text-decoration:none;font-weight:600">Email us (prefilled)</a>' +
      '<a href="' + wa + '" target="_blank" rel="noopener" style="padding:9px 14px;border-radius:6px;background:#16a34a;color:#fff;text-decoration:none;font-weight:600">WhatsApp</a>' +
      '</div>';
    var btn = form.querySelector('button');
    if (btn && btn.parentNode) { btn.parentNode.insertBefore(box, btn.nextSibling); }
    else { form.appendChild(box); }
  }

  function onSubmit(e) {
    var form = e.target;
    if (!form || form.getAttribute('action') === null) { return; }
    e.preventDefault();
    var btn = form.querySelector('button');
    var label = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }
    var ctrl = (typeof AbortController !== 'undefined') ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) { ctrl.abort(); } }, 12000);
    var opts = { method: 'POST', body: new FormData(form) };
    if (ctrl) { opts.signal = ctrl.signal; }
    fetch(AJAX, opts).then(function (r) {
      clearTimeout(timer);
      if (!r.ok) { throw new Error('HTTP ' + r.status); }
      return r.json().catch(function () { return {}; });
    }).then(function (j) {
      if (j && (j.success === false || j.success === 'false')) {
        throw new Error('relay rejected');
      }
      location.href = NEXT;
    }).catch(function () {
      clearTimeout(timer);
      if (btn) { btn.disabled = false; btn.textContent = label || 'Send Inquiry'; }
      showFallback(form, 'relay');
    });
  }

  function mount() {
    if (document.getElementById('jlcc-inquiry')) { return; }
    var section = document.createElement('section');
    section.id = 'jlcc-inquiry';
    section.innerHTML = [
      '<div style="max-width:960px;margin:0 auto">',
      '<h2>Request a Quote</h2>',
      '<p style="margin:0 0 18px;color:#475569;font-size:14px">Send your specification and quantity - we reply with price, lead time and packing.</p>',
      '<form action="' + ACTION + '" method="POST">',
      '<input type="hidden" name="_subject" value="Inquiry from ' + location.pathname + '">',
      '<input type="hidden" name="_captcha" value="false">',
      '<input type="hidden" name="_template" value="table">',
      '<input type="hidden" name="_next" value="' + NEXT + '">',
      '<input type="hidden" name="source_page" value="' + location.href + '">',
      '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">Your Name *<br><input type="text" name="name" required style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">Company<br><input type="text" name="company" style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '</div>',
      '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">Email *<br><input type="email" name="email" required style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">WhatsApp / Phone<br><input type="text" name="phone" style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '</div>',
      '<label style="display:block;font-size:12px;color:#334155">Requirement *<br><textarea name="message" required style="width:100%;min-height:110px;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></textarea></label>',
      '<button type="submit" style="margin-top:12px;padding:12px 22px;border:0;border-radius:6px;background:#2563eb;color:#fff;font-size:15px;font-weight:600;cursor:pointer">Send Inquiry</button>',
      '<p style="margin:10px 0 0;font-size:12px;color:#64748b">Typical reply within 2 hours on business days. Or WhatsApp +86 153 3900 5193.</p>',
      '</form>',
      '</div>'
    ].join('');
    section.setAttribute('style', 'padding:40px 16px;background:#f1f5f9;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif');
    var footer = document.querySelector('footer');
    if (footer && footer.parentNode) { footer.parentNode.insertBefore(section, footer); }
    else { document.body.appendChild(section); }
    var form = section.querySelector('form');
    if (form) { form.addEventListener('submit', onSubmit); }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
"""

CB_RE = re.compile(r"(assets/inquiry-form\.js)(?=[\"'])")


def fix_cb(s):
    return CB_RE.subn(r"\1?v=2", s)


REPORT = []


def fix_blog(s, body):
    if MARK in s:
        return s, False
    m = BLOG_ANCHOR.search(s)
    if not m:
        return s, False
    new = MARK + "\n" + body + "\n            "
    s = s[:m.start()] + new + s[m.end():]
    return s, True


def fix_titles(s, spec):
    title, h1, desc = spec
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, s, count=1, flags=re.S)
    s = re.sub(r"(?is)(<h1[^>]*>).*?(</h1>)",
               lambda m: m.group(1) + h1 + m.group(2), s, count=1)
    s = re.sub(r'(<meta name="description" content=").*?(">)',
               lambda m: m.group(1) + desc + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=").*?(">)',
               lambda m: m.group(1) + h1 + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=").*?(">)',
               lambda m: m.group(1) + desc + m.group(2), s, count=1)
    s = re.sub(r'(<meta name="twitter:title" content=").*?(">)',
               lambda m: m.group(1) + h1 + m.group(2), s, count=1)
    return s


def fix_temps(name, s):
    out = []
    for a, b in TEMP_SPECIAL:
        if a in s:
            s = s.replace(a, b)
            out.append("special: " + a[:52])
    def sub(m):
        ctx = s[max(0, m.start() - 90):m.end() + 60].lower()
        if any(w in ctx for w in TEMP_EXCL):
            return m.group(0)
        out.append("range: 120->90 at %d" % m.start())
        return m.group(1) + "90" + m.group(3)
    s = TEMP_RE.sub(sub, s)
    return s, out


def main():
    root = pathlib.Path(".")
    stats = {"blog_rewritten": 0, "titles_changed": 0, "temp_edits": 0,
             "files_written": 0, "js_written": 0, "missing": 0}

    for name, body in BLOGS.items():
        p = root / name
        if not p.exists():
            print("MISSING", name)
            stats["missing"] += 1
            continue
        s = orig = p.read_text(encoding="utf-8", errors="replace")
        if name in TITLES:
            s = fix_titles(s, TITLES[name])
        s, ok = fix_blog(s, body)
        if ok:
            stats["blog_rewritten"] += 1
            stats["titles_changed"] += name in TITLES
        if s != orig:
            p.write_text(s, encoding="utf-8", newline="")
            stats["files_written"] += 1

    stats["std_edits"] = 0
    for p in sorted(root.glob("*.html")):
        s = orig = p.read_text(encoding="utf-8", errors="replace")
        s, edits = fix_temps(p.name, s)
        s, shits = fix_std(s)
        s, n_cb = fix_cb(s)
        stats["cb_edits"] = stats.get("cb_edits", 0) + n_cb
        for e in edits:
            REPORT.append("%-46s %s" % (p.name, e))
        stats["temp_edits"] += len(edits)
        stats["std_edits"] += len(shits)
        if s != orig:
            p.write_text(s, encoding="utf-8", newline="")
            stats["files_written"] += 1

    js = root / JS_PATH
    if js.exists():
        cur = js.read_text(encoding="utf-8", errors="replace")
        if cur.strip() != NEW_JS.strip():
            js.write_text(NEW_JS, encoding="utf-8", newline="")
            stats["js_written"] = 1

    for k in sorted(stats):
        print("%-16s %d" % (k, stats[k]))
    print()
    for line in REPORT:
        print("  " + line)

    # verification
    print()
    left = 0
    for p in sorted(root.glob("*.html")):
        s = p.read_text(encoding="utf-8", errors="replace")
        for m in TEMP_RE.finditer(s):
            ctx = s[max(0, m.start() - 90):m.end() + 60].lower()
            if not any(w in ctx for w in TEMP_EXCL):
                left += 1
                print("  STILL BAD %s: %s" % (p.name, m.group(0)))
    print("operating-range 120C left:", left)
    print("IEC 62541 left:", sum(p.read_text(encoding="utf-8", errors="replace").count("62541")
                                 for p in root.glob("*.html")))
    print("blog pages with b7 marker:",
          sum(1 for p in root.glob("*.html")
              if MARK in p.read_text(encoding="utf-8", errors="replace")))


if __name__ == "__main__":
    main()
