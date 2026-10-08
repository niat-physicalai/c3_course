<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Practice part.</strong> Model a simple parametric part, such as a bracket or a phone stand, with at least three named driver parameters, one formula parameter and fully constrained sketches. Change each driver and confirm everything follows.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Parameter table.</strong> Write the parameter table for your own enclosure: drivers from your C3 board and C0 concept, followers as formulas, with a comment on each.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Two-part enclosure.</strong> Build it with Steps 1–10: parameters, sketch, block, fillets, shell, split, openings. Add at least the display and button openings from your C0 concept.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Change test.</strong> Change your board width by 2 mm and your wall thickness by 0.5 mm, one at a time. Record which features, if any, failed, and how you fixed them.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> your practice part and two-part enclosure (.f3d and .step exports), the parameter table, and your change-test notes, saved in your design pack as E0-cad/.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your enclosure model and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every sketch in the model is fully constrained (no blue geometry). — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every dimension shows <strong>fx:</strong>, using a parameter or formula, not a typed number. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every user parameter has a comment. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. The board's width, length and height are drivers, and the outer size is calculated from them. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. The enclosure is split into two named bodies, base and lid. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The measured inner cavity equals the calculated cavity size. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Changing pcb\_w by 2 mm rebuilds the whole model with no errors. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. Changing wall by 0.5 mm rebuilds the whole model with no errors. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. The timeline order is: block, fillets, shell, split, openings. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">10. The openings stay correctly placed after a size change. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A board is 38 mm wide. Clearance is 0.5 mm per side and walls are 1.5 mm. What is the enclosure's outer width?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. 39 mm</li><li style="margin:6px 0;">B. 41 mm</li><li style="margin:6px 0;">C. 42 mm</li><li style="margin:6px 0;">D. 44 mm</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> 38 + 2 × 0.5 + 2 × 1.5 = 42 mm. <strong>A</strong> is the inner cavity only. <strong>B</strong> adds the walls but forgets the clearance. <strong>D</strong> would be the result for a 40 mm board.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A sketch's lines are still blue after all dimensions are added. What does that mean, and what should you do?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The sketch is fine; blue is the default colour.</li><li style="margin:6px 0;">B. The sketch has too many constraints; delete some.</li><li style="margin:6px 0;">C. The model needs to be saved.</li><li style="margin:6px 0;">D. Something can still move; add the missing constraint or dimension until every line turns black.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>D.</strong> In Fusion, blue means under-constrained. <strong>A</strong> is wrong: fully constrained geometry turns black. <strong>B</strong> describes over-constraint, which Fusion refuses to apply rather than showing blue. <strong>C</strong> is unrelated.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A fillet fails after a parameter change. What is the most likely cause, and fix?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The edge it referred to no longer exists or has changed; re-select the edge, and consider moving the fillet earlier in the timeline.</li><li style="margin:6px 0;">B. The fillet radius is too small; increase it.</li><li style="margin:6px 0;">C. Fusion cannot fillet after a change; delete the fillet.</li><li style="margin:6px 0;">D. The model needs more parameters.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> Features refer to the edges and faces made by earlier ones, and a change can remove or replace them. Fixing the reference, and keeping the order "big shapes first, details last", solves most such failures. <strong>B</strong> may occasionally matter, but it is not the usual cause. <strong>C</strong> is false. <strong>D</strong> does not touch the broken reference.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> Why are the case's corners filleted before it is split into a lid and a base?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Fillets cannot be applied after a split.</li><li style="margin:6px 0;">B. One fillet on one body gives the lid and base exactly matching corners.</li><li style="margin:6px 0;">C. It makes the file smaller.</li><li style="margin:6px 0;">D. Split Body needs rounded corners.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> One feature on one body guarantees the two parts match. Filleting them separately risks different radii or references. <strong>A</strong>, <strong>C</strong> and <strong>D</strong> are not true.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> Which parameter should be a formula rather than a typed value?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. pcb\_w, the board width</li><li style="margin:6px 0;">B. wall, the wall thickness</li><li style="margin:6px 0;">C. clearance, the air gap</li><li style="margin:6px 0;">D. outer\_w, the enclosure's outer width</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>D.</strong> The outer width follows from the board, clearance and wall, so it should be calculated from them. <strong>A</strong>, <strong>B</strong> and <strong>C</strong> are drivers: values you choose or take from the board, which the rest of the model follows.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>6.</strong> You want Shell to turn a solid block into a closed hollow box, to split later. What do you select in the Shell dialog?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The top face</li><li style="margin:6px 0;">B. The body, with no face selected</li><li style="margin:6px 0;">C. All six faces</li><li style="margin:6px 0;">D. The sketch the block was made from</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Selecting the body hollows it without removing a face, leaving a closed box. <strong>A</strong> removes the top, giving an open tray. <strong>C</strong> would remove every face and leave nothing to shell. <strong>D</strong> is not a valid Shell input.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>7.</strong> You cut the display window into the lid, and the cut also goes through the floor of the base. What setting fixes it?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. In the cut's Extrude dialog, leave only lid ticked under <strong>Objects To Cut</strong>.</li><li style="margin:6px 0;">B. Make the window smaller.</li><li style="margin:6px 0;">C. Move the window sketch onto the base.</li><li style="margin:6px 0;">D. Delete the base and model it again.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> Objects To Cut limits which bodies a cut can touch. <strong>B</strong> does not stop the cut going through. <strong>C</strong> makes it worse. <strong>D</strong> throws away work for a one-click fix.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="E1-materials-colour-rendering.md">E1 — Materials, Colour and Rendering</a> you will choose what the enclosure is printed in and capture its presentation image. Then, in E2, you will bring the board STEP you exported in C3 into this model and fit it inside.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Autodesk. Education software overview (free, one-year access for eligible students and educators, renewable while eligible). https://www.autodesk.com/education/edu-software/overview</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Onshape. Variable Studios (help documentation for defining and sharing variables across part studios). https://cad.onshape.com/help/Content/VariableStudio/variable\_studio.htm</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Autodesk. How to Create and Edit Parameters in Fusion for Simplified Design Control (user parameters: name, unit, value, comment). https://www.autodesk.com/products/fusion-360/blog/mastering-fusion-parameters-a-guide-for-simplified-design-control/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Autodesk. Fusion Help. https://help.autodesk.com/view/fusion360/ENU/</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
