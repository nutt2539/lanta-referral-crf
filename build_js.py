# -*- coding: utf-8 -*-
"""
JavaScript Engine Generator module for Online CRF (Forms 1, 2, 3, 4)
"""

def get_js():
    return """
    // --- Online CRF JavaScript Engine ---

    // Global Active Tab State (1: Form 1, 2: Form 2, 3: Form 3, 4: Form 4)
    let currentTab = 1;

    // --- Global Deselectable / Toggleable Radio Buttons ---
    function initToggleableRadios() {
        let _radioPrevChecked = null;
        let _radioActiveTarget = null;
        let _lastDownTime = 0;

        function findRadio(target) {
            if (!target) return null;
            if (target.type === 'radio') return target;
            const label = target.closest('label');
            if (label) {
                return label.querySelector('input[type="radio"]') || 
                       (label.htmlFor ? document.getElementById(label.htmlFor) : null);
            }
            return null;
        }

        function handlePointerDown(e) {
            const now = Date.now();
            if (now - _lastDownTime < 40) return;
            _lastDownTime = now;

            const radio = findRadio(e.target);
            if (radio && radio.type === 'radio') {
                _radioPrevChecked = radio.checked;
                _radioActiveTarget = radio;
            } else {
                _radioPrevChecked = null;
                _radioActiveTarget = null;
            }
        }

        document.addEventListener('pointerdown', handlePointerDown, true);
        document.addEventListener('mousedown', handlePointerDown, true);

        document.addEventListener('keydown', function(e) {
            if ((e.key === ' ' || e.key === 'Spacebar') && e.target && e.target.type === 'radio') {
                _radioPrevChecked = e.target.checked;
                _radioActiveTarget = e.target;
            }
        }, true);

        document.addEventListener('click', function(e) {
            let radio = null;
            if (e.target && e.target.type === 'radio') {
                radio = e.target;
            }
            if (radio && radio === _radioActiveTarget) {
                if (_radioPrevChecked === true) {
                    // Radio was already checked before interaction -> Deselect it!
                    e.preventDefault();
                    radio.checked = false;
                    _radioPrevChecked = false;
                    _radioActiveTarget = null;
                    radio.dispatchEvent(new Event('change', { bubbles: true }));
                } else {
                    _radioPrevChecked = true;
                }
            }
        }, true);
    }

    // Initialize on DOM load
    document.addEventListener('DOMContentLoaded', function() {
        initToggleableRadios();
        initSyncFields();
        initAutoSave();
        loadCaseIndex();
        
        // Automatic Screen Density Optimization
        autoAdjustScreenDensity();

        // Load latest case or default
        const lastCaseId = localStorage.getItem('online_crf_last_active_id');
        if (lastCaseId) {
            loadCase(lastCaseId);
        } else {
            document.getElementById('f1_study_id').value = '001';
            syncFields('study-id-sync', '001');
            const ambEl = document.getElementById('f2_amb_type');
            if (ambEl) ambEl.checked = true;
            updateDiseaseVisuals(null);
            calcAll();
        }
    });

    // --- Automatic Responsive Screen Adaptation (Auto-Fit) ---
    function autoAdjustScreenDensity() {
        const h = window.innerHeight;
        if (h <= 860) {
            document.body.classList.add('auto-compact');
        } else {
            document.body.classList.remove('auto-compact');
        }
    }
    window.addEventListener('resize', autoAdjustScreenDensity);

    // Compatibility shim
    function setScreenDensity(mode) {
        autoAdjustScreenDensity();
    }

    // --- Inclusion Criteria Disease Validation ---
    function validateInclusionDisease(shouldAlert = true) {
        const disease = getActiveDisease();
        if (!disease) {
            if (shouldAlert) {
                alert('⚠️ แจ้งเตือน: ในเกณฑ์การคัดเข้าข้อ 4 บังคับต้องเลือก 1 ใน 3 กลุ่มโรคเป้าหมาย\\n(1. STEMI / ACS, 2. Acute Ischemic Stroke หรือ 3. Severe Trauma)\\n\\nกรุณาติ๊กเลือกกลุ่มโรคก่อนดำเนินการต่อไป');
                const alertEl = document.getElementById('f1_inc4_disease_alert');
                if (alertEl) {
                    alertEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    alertEl.style.boxShadow = '0 0 14px rgba(244, 63, 94, 0.9)';
                    setTimeout(() => { alertEl.style.boxShadow = ''; }, 2500);
                }
            }
            return false;
        }
        return true;
    }

    // --- Tab Navigation ---
    function switchTab(tabIndex) {
        tabIndex = Number(tabIndex);
        if (tabIndex > 1) {
            if (!validateInclusionDisease(true)) {
                return;
            }
        }

        currentTab = tabIndex;
        document.querySelectorAll('.crf-page').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

        const targetPage = document.getElementById('page-form' + currentTab);
        const targetBtn = document.getElementById('tab-btn-' + currentTab);
        if (targetPage) targetPage.classList.add('active');
        if (targetBtn) targetBtn.classList.add('active');

        // Update progress indicator with dynamic form color
        const progressEl = document.getElementById('progress-bar');
        if (progressEl) {
            if (currentTab === 1) {
                progressEl.style.width = '25%';
                progressEl.style.backgroundColor = '#1e40af';
            } else if (currentTab === 2) {
                progressEl.style.width = '50%';
                progressEl.style.backgroundColor = '#0f766e';
            } else if (currentTab === 3) {
                progressEl.style.width = '75%';
                progressEl.style.backgroundColor = '#7e22ce';
            } else if (currentTab === 4) {
                progressEl.style.width = '100%';
                progressEl.style.backgroundColor = '#b91c1c';
            }
        }

        if (currentTab === 2) {
            pullT0T1FromForm1();
            autoDetectFerryOperate();
        } else if (currentTab === 3) {
            autoDetectFerryOperate();
        } else if (currentTab === 4) {
            calcForm4Timelines();
            updateEpidemiologicalAssessment();
        }

        updateBottomNav();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function updateBottomNav() {
        const prevBtn = document.getElementById('btn-nav-prev');
        const nextBtn = document.getElementById('btn-nav-next');
        if (!prevBtn || !nextBtn) return;

        if (currentTab === 1) {
            prevBtn.style.visibility = 'hidden';
            nextBtn.className = 'btn btn-theme-2';
            nextBtn.innerHTML = '<span>ถัดไป: ส่วนที่ 2 (Form 2) ➔</span>';
        } else if (currentTab === 2) {
            prevBtn.style.visibility = 'visible';
            prevBtn.innerHTML = '⬅ ย้อนกลับไปส่วนที่ 1 (Form 1)';
            nextBtn.className = 'btn btn-theme-3';
            nextBtn.innerHTML = '<span>ถัดไป: ส่วนที่ 3 (Form 3) ➔</span>';
        } else if (currentTab === 3) {
            prevBtn.style.visibility = 'visible';
            prevBtn.innerHTML = '⬅ ย้อนกลับไปส่วนที่ 2 (Form 2)';
            nextBtn.className = 'btn btn-theme-4';
            nextBtn.innerHTML = '<span>ถัดไป: ส่วนที่ 4 (Form 4) ➔</span>';
        } else if (currentTab === 4) {
            prevBtn.style.visibility = 'visible';
            prevBtn.innerHTML = '⬅ ย้อนกลับไปส่วนที่ 3 (Form 3)';
            nextBtn.className = 'btn btn-blue';
            nextBtn.innerHTML = '<span>💾 บันทึกข้อมูลเคสนี้</span>';
        }
    }

    function nextTab() {
        if (currentTab === 1) {
            if (!validateInclusionDisease(true)) return;
            switchTab(2);
        }
        else if (currentTab === 2) switchTab(3);
        else if (currentTab === 3) switchTab(4);
        else if (currentTab === 4) {
            finalizeCaseSave();
        }
    }

    function finalizeCaseSave() {
        if (!validateInclusionDisease(true)) {
            switchTab(1);
            return;
        }
        saveCurrentCase(false);
        const studyId = document.getElementById('f1_study_id')?.value.trim() || '';
        const statusEl = document.getElementById('save-status');
        if (statusEl) {
            statusEl.innerHTML = '✓ บันทึกข้อมูลเคส LANTA_' + studyId + ' เรียบร้อยแล้ว';
            statusEl.style.display = 'inline-flex';
            setTimeout(() => statusEl.style.display = 'none', 3500);
        }
        alert('✓ บันทึกข้อมูลเคสผู้ป่วย ' + (studyId ? 'LANTA_' + studyId : '') + ' เรียบร้อยแล้ว');
    }

    function prevTab() {
        if (currentTab === 4) switchTab(3);
        else if (currentTab === 3) switchTab(2);
        else if (currentTab === 2) switchTab(1);
    }

    // --- Synchronize Identifiers across Form 1, 2, 3, 4 ---
    function initSyncFields() {
        const syncMap = [
            { class: 'study-id-sync', name: 'STUDY_ID' },
            { class: 'refer-id-sync', name: 'Refer_ID' },
            { class: 'hn-sync', name: 'HN' },
            { class: 'vn-sync', name: 'VN' },
            { class: 'date-sync', name: 'Date' },
            { class: 'abs-sync', name: 'Abstractor' }
        ];

        syncMap.forEach(item => {
            const inputs = document.querySelectorAll('.' + item.class);
            inputs.forEach(input => {
                input.addEventListener('input', function() {
                    const val = this.value;
                    inputs.forEach(target => {
                        if (target !== input) target.value = val;
                    });
                    scheduleAutoSave();
                });
            });
        });
    }

    function syncFields(className, val) {
        document.querySelectorAll('.' + className).forEach(el => el.value = val);
    }

    function getActiveDisease() {
        const stemi = document.getElementById('f1_inc4_stemi')?.checked;
        const ais = document.getElementById('f1_inc4_ais')?.checked;
        const trauma = document.getElementById('f1_inc4_trauma')?.checked;
        if (stemi) return 'stemi';
        if (ais) return 'ais';
        if (trauma) return 'trauma';
        return null;
    }

    function syncDiseaseGroup() {
        const disease = getActiveDisease();
        
        const inc4RadioYes = document.querySelector('input[name="f1_inc4"][value="yes"]');
        const inc4RadioNo = document.querySelector('input[name="f1_inc4"][value="no"]');
        if (disease) {
            if (inc4RadioYes) inc4RadioYes.checked = true;
            if (inc4RadioNo) inc4RadioNo.checked = false;
        } else {
            if (inc4RadioYes && inc4RadioYes.checked) inc4RadioYes.checked = false;
        }

        applyDiseaseIsolation(disease);
        updateDiseaseVisuals(disease);

        calcScreening();
        calcTimelines();
        calcAll();
        scheduleAutoSave();
    }

    function onInc4Change() {
        const val = document.querySelector('input[name="f1_inc4"]:checked')?.value;
        if (val === 'no') {
            // Patient does not meet criteria 4 -> uncheck all 3 disease options
            document.querySelectorAll('input[name="f1_target_disease"]').forEach(r => r.checked = false);
            syncDiseaseGroup();
        } else if (val === 'yes') {
            const disease = getActiveDisease();
            if (!disease) {
                alert('⚠️ ในเกณฑ์การคัดเข้าข้อ 4 บังคับต้องเลือก 1 ใน 3 กลุ่มโรคเป้าหมาย\\n(1. STEMI / ACS, 2. Acute Ischemic Stroke หรือ 3. Severe Trauma)\\n\\nกรุณาคลิกเลือกกลุ่มโรคทางด้านซ้าย');
                const alertEl = document.getElementById('f1_inc4_disease_alert');
                if (alertEl) {
                    alertEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    alertEl.style.boxShadow = '0 0 14px rgba(244, 63, 94, 0.9)';
                    setTimeout(() => { alertEl.style.boxShadow = ''; }, 2500);
                }
            }
        }
        calcScreening();
    }

    function applyDiseaseIsolation(disease) {
        // Clear disease-specific inputs that are not applicable to the active disease
        if (disease === 'ais') {
            // Stroke selected -> Clear STEMI & Trauma specific scores/fields
            const rts1 = document.getElementById('f1_rts_total'); if (rts1) rts1.value = '';
            const tCrit1 = document.getElementById('f1_trauma_acuity_crit'); if (tCrit1) tCrit1.checked = false;
            const tMod1 = document.getElementById('f1_trauma_acuity_mod'); if (tMod1) tMod1.checked = false;
            const m1 = document.getElementById('f1_trauma_mech1'); if (m1) m1.checked = false;
            const m2 = document.getElementById('f1_trauma_mech2'); if (m2) m2.checked = false;
            const m3 = document.getElementById('f1_trauma_mech3'); if (m3) m3.checked = false;

            document.querySelectorAll('input[name="f1_killip"]').forEach(r => r.checked = false);
            document.querySelectorAll('input[name="f4_killip"]').forEach(r => r.checked = false);
            const kFrom = document.getElementById('f4_delta_killip_from'); if (kFrom) kFrom.value = '';
            const kTo = document.getElementById('f4_delta_killip_to'); if (kTo) kTo.value = '';
            const kStab = document.getElementById('f4_killip_stable'); if (kStab) kStab.checked = false;
            const kDeter = document.getElementById('f4_killip_deter'); if (kDeter) kDeter.checked = false;

            const f4Crit = document.getElementById('f4_trauma_crit'); if (f4Crit) f4Crit.checked = false;
            const f4Mod = document.getElementById('f4_trauma_mod'); if (f4Mod) f4Mod.checked = false;
            const f4Rts = document.getElementById('f4_delta_rts'); if (f4Rts) f4Rts.value = '';
            const rStab = document.getElementById('f4_rts_stable'); if (rStab) rStab.checked = false;
            const rDeter = document.getElementById('f4_rts_deter'); if (rDeter) rDeter.checked = false;

            // Clear MSI (Stroke does not calculate MSI)
            const msi1 = document.getElementById('f1_msi'); if (msi1) msi1.value = '';
            const msi4 = document.getElementById('f4_msi'); if (msi4) msi4.value = '';
            const dMsi = document.getElementById('f4_delta_msi'); if (dMsi) dMsi.value = '';
            const ms1 = document.getElementById('f4_msi_stable'); if (ms1) ms1.checked = false;
            const ms2 = document.getElementById('f4_msi_deter'); if (ms2) ms2.checked = false;

            // Clear & Disable Baseline Hct (Trauma only)
            const hct1 = document.getElementById('f1_hct');
            if (hct1) { hct1.value = ''; hct1.disabled = true; hct1.placeholder = 'N/A'; }

            // Clear & Disable Trauma Resuscitation (Trauma only)
            ['f1_resusc_txa', 'f1_resusc_splint', 'f1_resusc_pelvic', 'f1_resusc_icd'].forEach(id => {
                const el = document.getElementById(id);
                if (el) { el.checked = false; el.disabled = true; }
            });

            const wire = document.getElementById('f4_pci_wire_time'); if (wire) wire.value = '';
            const d2b = document.getElementById('f4_pci_d2b_min'); if (d2b) d2b.value = '';
            const pciAch = document.getElementById('f4_pci_achieved'); if (pciAch) pciAch.checked = false;
            const pciMis = document.getElementById('f4_pci_missed'); if (pciMis) pciMis.checked = false;

            const trCt = document.getElementById('f4_trauma_ct_time'); if (trCt) trCt.value = '';
            const d2ct = document.getElementById('f4_trauma_d2ct_min'); if (d2ct) d2ct.value = '';
            const orT = document.getElementById('f4_or_time'); if (orT) orT.value = '';
            const d2or = document.getElementById('f4_trauma_d2or_min'); if (d2or) d2or.value = '';
            const orAch = document.getElementById('f4_trauma_achieved'); if (orAch) orAch.checked = false;
            const orMis = document.getElementById('f4_trauma_missed'); if (orMis) orMis.checked = false;

        } else if (disease === 'stemi') {
            // STEMI selected -> Clear Stroke & Trauma specific scores/fields
            const rts1 = document.getElementById('f1_rts_total'); if (rts1) rts1.value = '';
            const tCrit1 = document.getElementById('f1_trauma_acuity_crit'); if (tCrit1) tCrit1.checked = false;
            const tMod1 = document.getElementById('f1_trauma_acuity_mod'); if (tMod1) tMod1.checked = false;
            const m1 = document.getElementById('f1_trauma_mech1'); if (m1) m1.checked = false;
            const m2 = document.getElementById('f1_trauma_mech2'); if (m2) m2.checked = false;
            const m3 = document.getElementById('f1_trauma_mech3'); if (m3) m3.checked = false;

            document.querySelectorAll('input[name="f1_stroke_gcs"]').forEach(r => r.checked = false);
            document.querySelectorAll('input[name="f4_stroke_gcs"]').forEach(r => r.checked = false);

            const f4Crit = document.getElementById('f4_trauma_crit'); if (f4Crit) f4Crit.checked = false;
            const f4Mod = document.getElementById('f4_trauma_mod'); if (f4Mod) f4Mod.checked = false;
            const f4Rts = document.getElementById('f4_delta_rts'); if (f4Rts) f4Rts.value = '';
            const rStab = document.getElementById('f4_rts_stable'); if (rStab) rStab.checked = false;
            const rDeter = document.getElementById('f4_rts_deter'); if (rDeter) rDeter.checked = false;

            // Clear & Disable Baseline Hct (Trauma only)
            const hct1 = document.getElementById('f1_hct');
            if (hct1) { hct1.value = ''; hct1.disabled = true; hct1.placeholder = 'N/A'; }

            // Clear & Disable Trauma Resuscitation (Trauma only)
            ['f1_resusc_txa', 'f1_resusc_splint', 'f1_resusc_pelvic', 'f1_resusc_icd'].forEach(id => {
                const el = document.getElementById(id);
                if (el) { el.checked = false; el.disabled = true; }
            });

            const rtpa = document.getElementById('f4_rtpa_time'); if (rtpa) rtpa.value = '';
            const o2n = document.getElementById('f4_stroke_o2n_min'); if (o2n) o2n.value = '';
            const sAch = document.getElementById('f4_stroke_achieved'); if (sAch) sAch.checked = false;
            const sMis = document.getElementById('f4_stroke_missed'); if (sMis) sMis.checked = false;

            const trCt = document.getElementById('f4_trauma_ct_time'); if (trCt) trCt.value = '';
            const d2ct = document.getElementById('f4_trauma_d2ct_min'); if (d2ct) d2ct.value = '';
            const orT = document.getElementById('f4_or_time'); if (orT) orT.value = '';
            const d2or = document.getElementById('f4_trauma_d2or_min'); if (d2or) d2or.value = '';
            const orAch = document.getElementById('f4_trauma_achieved'); if (orAch) orAch.checked = false;
            const orMis = document.getElementById('f4_trauma_missed'); if (orMis) orMis.checked = false;

            // Recalculate MSI for STEMI
            calcVitals();
            calcKrabiVitals();

        } else if (disease === 'trauma') {
            // Trauma selected -> Clear STEMI & Stroke specific scores/fields
            document.querySelectorAll('input[name="f1_killip"]').forEach(r => r.checked = false);
            document.querySelectorAll('input[name="f1_stroke_gcs"]').forEach(r => r.checked = false);

            document.querySelectorAll('input[name="f4_killip"]').forEach(r => r.checked = false);
            const kFrom = document.getElementById('f4_delta_killip_from'); if (kFrom) kFrom.value = '';
            const kTo = document.getElementById('f4_delta_killip_to'); if (kTo) kTo.value = '';
            const kStab = document.getElementById('f4_killip_stable'); if (kStab) kStab.checked = false;
            const kDeter = document.getElementById('f4_killip_deter'); if (kDeter) kDeter.checked = false;

            document.querySelectorAll('input[name="f4_stroke_gcs"]').forEach(r => r.checked = false);

            // Clear MSI (Trauma does not calculate MSI)
            const msi1 = document.getElementById('f1_msi'); if (msi1) msi1.value = '';
            const msi4 = document.getElementById('f4_msi'); if (msi4) msi4.value = '';
            const dMsi = document.getElementById('f4_delta_msi'); if (dMsi) dMsi.value = '';
            const ms1 = document.getElementById('f4_msi_stable'); if (ms1) ms1.checked = false;
            const ms2 = document.getElementById('f4_msi_deter'); if (ms2) ms2.checked = false;

            // Enable Baseline Hct (Trauma only)
            const hct1 = document.getElementById('f1_hct');
            if (hct1) { hct1.disabled = false; hct1.placeholder = ''; }

            // Enable Trauma Resuscitation (Trauma only)
            ['f1_resusc_txa', 'f1_resusc_splint', 'f1_resusc_pelvic', 'f1_resusc_icd'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.disabled = false;
            });

            const wire = document.getElementById('f4_pci_wire_time'); if (wire) wire.value = '';
            const d2b = document.getElementById('f4_pci_d2b_min'); if (d2b) d2b.value = '';
            const pciAch = document.getElementById('f4_pci_achieved'); if (pciAch) pciAch.checked = false;
            const pciMis = document.getElementById('f4_pci_missed'); if (pciMis) pciMis.checked = false;

            const rtpa = document.getElementById('f4_rtpa_time'); if (rtpa) rtpa.value = '';
            const o2n = document.getElementById('f4_stroke_o2n_min'); if (o2n) o2n.value = '';
            const sAch = document.getElementById('f4_stroke_achieved'); if (sAch) sAch.checked = false;
            const sMis = document.getElementById('f4_stroke_missed'); if (sMis) sMis.checked = false;

        } else {
            // None selected -> Clear all disease-specific fields
            const rts1 = document.getElementById('f1_rts_total'); if (rts1) rts1.value = '';
            const tCrit1 = document.getElementById('f1_trauma_acuity_crit'); if (tCrit1) tCrit1.checked = false;
            const tMod1 = document.getElementById('f1_trauma_acuity_mod'); if (tMod1) tMod1.checked = false;
            document.querySelectorAll('input[name="f1_killip"]').forEach(r => r.checked = false);
            document.querySelectorAll('input[name="f1_stroke_gcs"]').forEach(r => r.checked = false);

            document.querySelectorAll('input[name="f4_killip"]').forEach(r => r.checked = false);
            const kFrom = document.getElementById('f4_delta_killip_from'); if (kFrom) kFrom.value = '';
            const kTo = document.getElementById('f4_delta_killip_to'); if (kTo) kTo.value = '';
            const kStab = document.getElementById('f4_killip_stable'); if (kStab) kStab.checked = false;
            const kDeter = document.getElementById('f4_killip_deter'); if (kDeter) kDeter.checked = false;

            document.querySelectorAll('input[name="f4_stroke_gcs"]').forEach(r => r.checked = false);
            const f4Crit = document.getElementById('f4_trauma_crit'); if (f4Crit) f4Crit.checked = false;
            const f4Mod = document.getElementById('f4_trauma_mod'); if (f4Mod) f4Mod.checked = false;
            const f4Rts = document.getElementById('f4_delta_rts'); if (f4Rts) f4Rts.value = '';
            const rStab = document.getElementById('f4_rts_stable'); if (rStab) rStab.checked = false;
            const rDeter = document.getElementById('f4_rts_deter'); if (rDeter) rDeter.checked = false;

            // Clear MSI
            const msi1 = document.getElementById('f1_msi'); if (msi1) msi1.value = '';
            const msi4 = document.getElementById('f4_msi'); if (msi4) msi4.value = '';
            const dMsi = document.getElementById('f4_delta_msi'); if (dMsi) dMsi.value = '';
            const ms1 = document.getElementById('f4_msi_stable'); if (ms1) ms1.checked = false;
            const ms2 = document.getElementById('f4_msi_deter'); if (ms2) ms2.checked = false;

            // Clear & Disable Baseline Hct
            const hct1 = document.getElementById('f1_hct');
            if (hct1) { hct1.value = ''; hct1.disabled = true; hct1.placeholder = 'N/A'; }

            // Clear & Disable Trauma Resuscitation
            ['f1_resusc_txa', 'f1_resusc_splint', 'f1_resusc_pelvic', 'f1_resusc_icd'].forEach(id => {
                const el = document.getElementById(id);
                if (el) { el.checked = false; el.disabled = true; }
            });

            const wire = document.getElementById('f4_pci_wire_time'); if (wire) wire.value = '';
            const d2b = document.getElementById('f4_pci_d2b_min'); if (d2b) d2b.value = '';
            const pciAch = document.getElementById('f4_pci_achieved'); if (pciAch) pciAch.checked = false;
            const pciMis = document.getElementById('f4_pci_missed'); if (pciMis) pciMis.checked = false;

            const rtpa = document.getElementById('f4_rtpa_time'); if (rtpa) rtpa.value = '';
            const o2n = document.getElementById('f4_stroke_o2n_min'); if (o2n) o2n.value = '';
            const sAch = document.getElementById('f4_stroke_achieved'); if (sAch) sAch.checked = false;
            const sMis = document.getElementById('f4_stroke_missed'); if (sMis) sMis.checked = false;

            const trCt = document.getElementById('f4_trauma_ct_time'); if (trCt) trCt.value = '';
            const d2ct = document.getElementById('f4_trauma_d2ct_min'); if (d2ct) d2ct.value = '';
            const orT = document.getElementById('f4_or_time'); if (orT) orT.value = '';
            const d2or = document.getElementById('f4_trauma_d2or_min'); if (d2or) d2or.value = '';
            const orAch = document.getElementById('f4_trauma_achieved'); if (orAch) orAch.checked = false;
            const orMis = document.getElementById('f4_trauma_missed'); if (orMis) orMis.checked = false;
        }
    }

    function updateDiseaseVisuals(disease) {
        const rows = document.querySelectorAll('.disease-specific-row');
        rows.forEach(row => {
            const rowDisease = row.getAttribute('data-disease');
            if (!disease) {
                row.style.opacity = '1';
                row.style.pointerEvents = 'auto';
                row.style.background = '';
                row.querySelectorAll('input').forEach(i => i.disabled = false);
            } else if (rowDisease === disease) {
                row.style.opacity = '1';
                row.style.pointerEvents = 'auto';
                row.style.background = '#f0fdf4';
                row.querySelectorAll('input').forEach(i => i.disabled = false);
            } else {
                row.style.opacity = '0.35';
                row.style.pointerEvents = 'none';
                row.style.background = '#f8fafc';
                row.querySelectorAll('input').forEach(i => {
                    i.disabled = true;
                    if (i.type === 'radio' || i.type === 'checkbox') i.checked = false;
                });
            }
        });

        // Individual cell visuals for Form 1 and Form 4
        const isNone = !disease;
        const setCellState = (lblId, valId, isMatch) => {
            const lbl = document.getElementById(lblId);
            const val = document.getElementById(valId);
            if (!lbl || !val) return;
            if (isNone) {
                lbl.style.opacity = '1';
                lbl.style.background = '#f8fafc';
                val.style.opacity = '1';
                val.style.pointerEvents = 'auto';
                val.querySelectorAll('input').forEach(i => i.disabled = false);
            } else if (isMatch) {
                lbl.style.opacity = '1';
                lbl.style.background = '#f0fdf4';
                val.style.opacity = '1';
                val.style.pointerEvents = 'auto';
                val.querySelectorAll('input').forEach(i => i.disabled = false);
            } else {
                lbl.style.opacity = '0.35';
                lbl.style.background = '#f8fafc';
                val.style.opacity = '0.35';
                val.style.pointerEvents = 'none';
                val.querySelectorAll('input').forEach(i => {
                    i.disabled = true;
                    if (i.type === 'radio' || i.type === 'checkbox') i.checked = false;
                });
            }
        };

        setCellState('f1_label_hct', 'f1_cell_hct', disease === 'trauma');
        setCellState('f4_cell_killip_lbl', 'f4_cell_killip_val', disease === 'stemi');
        setCellState('f4_cell_stroke_lbl', 'f4_cell_stroke_val', disease === 'ais');
        setCellState('f4_cell_trauma_lbl', 'f4_cell_trauma_val', disease === 'trauma');
        setCellState('f4_cell_msi_lbl', 'f4_cell_msi_val', disease === 'stemi');

        // Form 1 Item 4 Mandatory Disease Visual Alert / Badge
        const inc4Alert = document.getElementById('f1_inc4_disease_alert');
        const inc4Badge = document.getElementById('f1_inc4_disease_selected_badge');
        const inc4Name = document.getElementById('f1_active_disease_name');
        const inc4Cell = document.getElementById('f1_inc4_cell');

        if (!disease) {
            if (inc4Alert) inc4Alert.style.display = 'flex';
            if (inc4Badge) inc4Badge.style.display = 'none';
            if (inc4Cell) {
                inc4Cell.style.borderLeft = '4px solid #f43f5e';
                inc4Cell.style.background = '#fff5f5';
            }
        } else {
            if (inc4Alert) inc4Alert.style.display = 'none';
            if (inc4Badge) inc4Badge.style.display = 'inline-block';
            let dName = '';
            if (disease === 'stemi') dName = '1. STEMI / Acute Coronary Syndrome (ACS)';
            else if (disease === 'ais') dName = '2. Acute Ischemic Stroke (AIS)';
            else if (disease === 'trauma') dName = '3. Severe Trauma (อุบัติเหตุบาดเจ็บรุนแรง)';
            if (inc4Name) inc4Name.textContent = dName;
            if (inc4Cell) {
                inc4Cell.style.borderLeft = '4px solid #10b981';
                inc4Cell.style.background = '#f0fdf4';
            }
        }
    }

    // --- Automatic Ferry Operating Period Detection from T2 ---
    function updateFerryBadges(val, sourceTime = '') {
        const badgeF2 = document.getElementById('f2_ferry_operate_badge');
        const badgeF3 = document.getElementById('f3_ferry_shift_badge');
        let html = '';
        if (val === '0') {
            const timeInfo = sourceTime ? ` (T2: ${sourceTime} น.)` : '';
            html = `<span class="badge" style="background:#e0f2fe; color:#0369a1; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:700; display:inline-flex; align-items:center; gap:4px;">⚡ Auto${timeInfo}: 0 = Scheduled Daytime (05:00–24:00 น.)</span>`;
        } else if (val === '1') {
            const timeInfo = sourceTime ? ` (T2: ${sourceTime} น.)` : '';
            html = `<span class="badge" style="background:#fef3c7; color:#b45309; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:700; display:inline-flex; align-items:center; gap:4px;">⚡ Auto${timeInfo}: 1 = Standby Off-Hour (24:00–05:00 น.)</span>`;
        } else {
            html = `<span style="color:#64748b; font-size:11px; font-weight:normal;">(รอระบุเวลา T2 เพื่อคำนวณรอบการเดินแพ)</span>`;
        }
        if (badgeF2) badgeF2.innerHTML = html;
        if (badgeF3) badgeF3.innerHTML = html;
    }

    function autoDetectFerryOperate() {
        const t2Time = document.getElementById('f2_t2_time')?.value;
        const radF2_0 = document.getElementById('f2_ferry_operate_0');
        const radF2_1 = document.getElementById('f2_ferry_operate_1');
        const radF3_0 = document.getElementById('f3_ferry_shift_0');
        const radF3_1 = document.getElementById('f3_ferry_shift_1');

        if (!t2Time) {
            const curVal = document.querySelector('input[name="f2_ferry_operate"]:checked')?.value || 
                           document.querySelector('input[name="f3_ferry_shift"]:checked')?.value;
            if (curVal !== undefined && curVal !== '') {
                updateFerryBadges(curVal);
            } else {
                updateFerryBadges(null);
            }
            return;
        }

        const parts = t2Time.split(':').map(Number);
        if (parts.length >= 2 && !isNaN(parts[0])) {
            const hour = parts[0];
            // 05:00 to 23:59 -> 0 (Scheduled Daytime 05:00-24:00), 00:00 to 04:59 -> 1 (Standby Off-Hour 24:00-05:00)
            const isDaytime = (hour >= 5 && hour < 24);
            const targetVal = isDaytime ? '0' : '1';

            if (radF2_0 && radF2_1) {
                radF2_0.checked = isDaytime;
                radF2_1.checked = !isDaytime;
            }
            if (radF3_0 && radF3_1) {
                radF3_0.checked = isDaytime;
                radF3_1.checked = !isDaytime;
            }

            updateFerryBadges(targetVal, t2Time);
            scheduleAutoSave();
        }
    }

    function syncFerryShiftFromF2() {
        const val = document.querySelector('input[name="f2_ferry_operate"]:checked')?.value;
        if (val !== undefined) {
            const radF3 = document.querySelector(`input[name="f3_ferry_shift"][value="${val}"]`);
            if (radF3) radF3.checked = true;
            updateFerryBadges(val);
            scheduleAutoSave();
        }
    }

    function syncFerryShiftFromF3() {
        const val = document.querySelector('input[name="f3_ferry_shift"]:checked')?.value;
        if (val !== undefined) {
            const radF2 = document.querySelector(`input[name="f2_ferry_operate"][value="${val}"]`);
            if (radF2) radF2.checked = true;
            updateFerryBadges(val);
            scheduleAutoSave();
        }
    }

    // --- En-route CPR Outcome & Duration Gating ---
    function toggleCprDetails() {
        const isCpr = document.querySelector('input[name="f2_ae_cpr"]:checked')?.value === '1';
        const box = document.getElementById('f2_cpr_details_box');
        const durInput = document.getElementById('f2_cpr_duration');
        const radRosc = document.getElementById('f2_cpr_outcome_rosc');
        const radOngoing = document.getElementById('f2_cpr_outcome_ongoing');

        if (box) {
            if (isCpr) {
                box.style.opacity = '1';
                box.style.pointerEvents = 'auto';
                if (durInput) durInput.disabled = false;
                if (radRosc) radRosc.disabled = false;
                if (radOngoing) radOngoing.disabled = false;
            } else {
                box.style.opacity = '0.35';
                box.style.pointerEvents = 'none';
                if (durInput) {
                    durInput.disabled = true;
                    durInput.value = '';
                }
                if (radRosc) {
                    radRosc.disabled = true;
                    radRosc.checked = false;
                }
                if (radOngoing) {
                    radOngoing.disabled = true;
                    radOngoing.checked = false;
                }
            }
        }
    }

    // --- Mortality Cause of Death & Timeline Gating ---
    function toggleMortalityDetails() {
        const mortEr = document.querySelector('input[name="f4_mort_er"]:checked')?.value;
        const mort24h = document.querySelector('input[name="f4_mort_24h"]:checked')?.value;

        const erTimeEl = document.getElementById('f4_mort_er_time');
        if (erTimeEl) {
            erTimeEl.disabled = (mortEr !== '1');
            if (mortEr !== '1') erTimeEl.value = '';
        }

        const d24DateEl = document.getElementById('f4_mort_24h_date');
        const d24TimeEl = document.getElementById('f4_mort_24h_time');
        if (d24DateEl) {
            d24DateEl.disabled = (mort24h !== '1');
            if (mort24h !== '1') d24DateEl.value = '';
        }
        if (d24TimeEl) {
            d24TimeEl.disabled = (mort24h !== '1');
            if (mort24h !== '1') d24TimeEl.value = '';
        }

        const isDeceased = (mort24h === '1' || mortEr === '1');
        const causeBox = document.getElementById('f4_mort_cause_container');
        if (causeBox) {
            if (isDeceased) {
                causeBox.style.opacity = '1';
                causeBox.style.pointerEvents = 'auto';
                causeBox.querySelectorAll('input').forEach(input => input.disabled = false);
            } else {
                causeBox.style.opacity = '0.35';
                causeBox.style.pointerEvents = 'none';
                causeBox.querySelectorAll('input').forEach(input => {
                    input.disabled = true;
                    if (input.type === 'radio' || input.type === 'checkbox') input.checked = false;
                    else input.value = '';
                });
            }
        }
        scheduleAutoSave();
    }

    // --- Automatic ED Shift Detection from T1 (Door-Out) ---
    function autoDetectShift() {
        // Primary source: T1 (Island ED Departure Time); fallback to T0 if T1 not set
        const t1Time = document.getElementById('f1_t1_time')?.value || document.getElementById('f2_t1_time')?.value;
        const sourceTime = t1Time || document.getElementById('f1_t0_time')?.value || document.getElementById('f2_t0_time')?.value;
        if (!sourceTime) return;
        const parts = sourceTime.split(':').map(Number);
        if (parts.length < 2 || isNaN(parts[0]) || isNaN(parts[1])) return;
        const totalMinutes = parts[0] * 60 + parts[1];

        let shift = null;
        if (totalMinutes >= 480 && totalMinutes < 960) {
            // 08:00 - 15:59: เวรเช้า (Morning)
            shift = 'morning';
        } else if (totalMinutes >= 960 && totalMinutes < 1440) {
            // 16:00 - 23:59: เวรบ่าย (Afternoon)
            shift = 'afternoon';
        } else {
            // 00:00 - 07:59: เวรดึก (Night)
            shift = 'night';
        }

        if (shift) {
            const radF1 = document.querySelector(`input[name="f1_shift"][value="${shift}"]`);
            if (radF1) radF1.checked = true;
            const radF3 = document.querySelector(`input[name="f3_ed_shift"][value="${shift}"]`);
            if (radF3) radF3.checked = true;
        }
    }

    // --- Synchronize Timestamps between forms ---
    function pullT0T1FromForm1() {
        const t0Date = document.getElementById('f1_t0_date')?.value || '';
        const t0Time = document.getElementById('f1_t0_time')?.value || '';
        let t1Date = document.getElementById('f1_t1_date')?.value || '';
        const t1Time = document.getElementById('f1_t1_time')?.value || '';

        // If T1 date is not set but T1 time and T0 date exist, default T1 date to T0 date
        if (!t1Date && t1Time && t0Date) {
            t1Date = t0Date;
            const f1T1D = document.getElementById('f1_t1_date');
            if (f1T1D) f1T1D.value = t0Date;
        }

        const f2_t0_d = document.getElementById('f2_t0_date');
        const f2_t0_t = document.getElementById('f2_t0_time');
        const f2_t1_d = document.getElementById('f2_t1_date');
        const f2_t1_t = document.getElementById('f2_t1_time');

        if (f2_t0_d && t0Date) f2_t0_d.value = t0Date;
        if (f2_t0_t && t0Time) f2_t0_t.value = t0Time;
        if (f2_t1_d && t1Date) f2_t1_d.value = t1Date;
        if (f2_t1_t && t1Time) f2_t1_t.value = t1Time;

        autoDetectShift();
        if (typeof calcForm2Timelines === 'function') calcForm2Timelines();
        autoDetectFerryOperate();
    }

    function syncT0() {
        const d = document.getElementById('f1_t0_date')?.value || '';
        const t = document.getElementById('f1_t0_time')?.value || '';
        const f2_d = document.getElementById('f2_t0_date');
        const f2_t = document.getElementById('f2_t0_time');
        if (f2_d) f2_d.value = d;
        if (f2_t) f2_t.value = t;
        autoDetectShift();
        if (typeof calcForm2Timelines === 'function') calcForm2Timelines();
    }

    function syncT0_fromF2() {
        const d = document.getElementById('f2_t0_date')?.value || '';
        const t = document.getElementById('f2_t0_time')?.value || '';
        const f1_d = document.getElementById('f1_t0_date');
        const f1_t = document.getElementById('f1_t0_time');
        if (f1_d) f1_d.value = d;
        if (f1_t) f1_t.value = t;
        autoDetectShift();
        if (typeof calcTimelines === 'function') calcTimelines();
    }

    function syncT1() {
        let d = document.getElementById('f1_t1_date')?.value || '';
        const t = document.getElementById('f1_t1_time')?.value || '';
        const t0_d = document.getElementById('f1_t0_date')?.value || '';
        if (!d && t && t0_d) {
            d = t0_d;
            const f1T1D = document.getElementById('f1_t1_date');
            if (f1T1D) f1T1D.value = d;
        }
        const f2_d = document.getElementById('f2_t1_date');
        const f2_t = document.getElementById('f2_t1_time');
        if (f2_d) f2_d.value = d;
        if (f2_t) f2_t.value = t;
        autoDetectShift();
        if (typeof calcForm2Timelines === 'function') calcForm2Timelines();
    }

    function syncT1_fromF2() {
        const d = document.getElementById('f2_t1_date')?.value || '';
        const t = document.getElementById('f2_t1_time')?.value || '';
        const f1_d = document.getElementById('f1_t1_date');
        const f1_t = document.getElementById('f1_t1_time');
        if (f1_d) f1_d.value = d;
        if (f1_t) f1_t.value = t;
        autoDetectShift();
        if (typeof calcTimelines === 'function') calcTimelines();
    }

    function syncT4() {
        const d = document.getElementById('f2_t4_date')?.value;
        const t = document.getElementById('f2_t4_time')?.value;
        const f4_d = document.getElementById('f4_t4_date');
        const f4_t = document.getElementById('f4_t4_time');
        if (f4_d) f4_d.value = d;
        if (f4_t) f4_t.value = t;
    }

    function syncT4_fromF4() {
        const d = document.getElementById('f4_t4_date')?.value;
        const t = document.getElementById('f4_t4_time')?.value;
        const f2_d = document.getElementById('f2_t4_date');
        const f2_t = document.getElementById('f2_t4_time');
        if (f2_d) f2_d.value = d;
        if (f2_t) f2_t.value = t;
    }

    function syncT5() {
        const d = document.getElementById('f2_t5_date')?.value;
        const t = document.getElementById('f2_t5_time')?.value;
        const f4_d = document.getElementById('f4_t5_date');
        const f4_t = document.getElementById('f4_t5_time');
        if (f4_d) f4_d.value = d;
        if (f4_t) f4_t.value = t;
    }

    function syncT5_fromF4() {
        const d = document.getElementById('f4_t5_date')?.value;
        const t = document.getElementById('f4_t5_time')?.value;
        const f2_d = document.getElementById('f2_t5_date');
        const f2_t = document.getElementById('f2_t5_time');
        if (f2_d) f2_d.value = d;
        if (f2_t) f2_t.value = t;
    }

    // --- Date/Time Parsing & Diff (in Minutes) ---
    function parseDateTime(dateStr, timeStr) {
        if (!timeStr) return null;
        if (!dateStr) dateStr = '2026-01-01'; // Default fallback date for intra-day
        const dParts = dateStr.split('-').map(Number);
        const tParts = timeStr.split(':').map(Number);
        if (dParts.length !== 3 || tParts.length < 2) return null;
        return new Date(dParts[0], dParts[1] - 1, dParts[2], tParts[0], tParts[1], tParts[2] || 0);
    }

    function diffMinutes(d1, t1, d2, t2) {
        if (!t1 || !t2) return null;
        // Cross-fill missing date from the other side if only one is provided
        if (!d1 && d2) d1 = d2;
        if (!d2 && d1) d2 = d1;
        if (!d1 && !d2) d1 = d2 = '2026-01-01';

        const dt1 = parseDateTime(d1, t1);
        const dt2 = parseDateTime(d2, t2);
        if (!dt1 || !dt2) return null;

        let diffMs = dt2.getTime() - dt1.getTime();

        // Midnight crossover handler:
        // If on same calendar day and dt2 < dt1, check if event started late night and ended morning
        if (diffMs < 0 && d1 === d2) {
            const [h1] = t1.split(':').map(Number);
            const [h2] = t2.split(':').map(Number);
            if (h1 >= 18 && h2 < 12) {
                diffMs += 24 * 60 * 60 * 1000;
            }
        }
        return Math.round(diffMs / 60000);
    }

    function setTimelineResult(inputId, ontimeRadioId, delayRadioId, diff, limit) {
        const inputEl = document.getElementById(inputId);
        const onEl = document.getElementById(ontimeRadioId);
        const delEl = document.getElementById(delayRadioId);

        if (diff === null) {
            if (inputEl) inputEl.value = '';
            if (onEl) onEl.checked = false;
            if (delEl) delEl.checked = false;
            return;
        }

        if (diff < 0) {
            if (inputEl) inputEl.value = 'เวลาไม่ถูกต้อง';
            if (onEl) onEl.checked = false;
            if (delEl) delEl.checked = false;
            return;
        }

        if (inputEl) inputEl.value = diff;
        if (diff <= limit) {
            if (onEl) onEl.checked = true;
            if (delEl) delEl.checked = false;
        } else {
            if (delEl) delEl.checked = true;
            if (onEl) onEl.checked = false;
        }
    }

    // --- FORM 1 CALCULATIONS ---
    function calcScreening() {
        const inc1 = document.querySelector('input[name="f1_inc1"]:checked')?.value;
        const inc2 = document.querySelector('input[name="f1_inc2"]:checked')?.value;
        const inc3 = document.querySelector('input[name="f1_inc3"]:checked')?.value;
        const inc4 = document.querySelector('input[name="f1_inc4"]:checked')?.value;
        const disease = getActiveDisease();

        const exc1 = document.querySelector('input[name="f1_exc1"]:checked')?.value;
        const exc2 = document.querySelector('input[name="f1_exc2"]:checked')?.value;
        const exc3 = document.querySelector('input[name="f1_exc3"]:checked')?.value;
        const exc4 = document.querySelector('input[name="f1_exc4"]:checked')?.value;
        const exc5 = document.querySelector('input[name="f1_exc5"]:checked')?.value;

        const isIncAllYes = (inc1 === 'yes' && inc2 === 'yes' && inc3 === 'yes' && inc4 === 'yes' && Boolean(disease));
        const isExcAnyYes = (exc1 === 'yes' || exc2 === 'yes' || exc3 === 'yes' || exc4 === 'yes' || exc5 === 'yes');

        const badge = document.getElementById('screening_badge');
        if (badge) badge.style.display = 'inline-block';

        if (isIncAllYes && !isExcAnyYes && exc1 && exc2 && exc3 && exc4 && exc5) {
            document.getElementById('f1_eligible_yes').checked = true;
            if (badge) {
                badge.className = 'badge-calc badge-ontime';
                badge.textContent = '✓ ผ่านเกณฑ์การวิจัย';
            }
        } else if (inc1 === 'no' || inc2 === 'no' || inc3 === 'no' || inc4 === 'no' || isExcAnyYes) {
            document.getElementById('f1_eligible_no').checked = true;
            if (badge) {
                badge.className = 'badge-calc badge-delay';
                badge.textContent = '✗ ไม่ผ่านเกณฑ์ (คัดออก)';
            }
        } else if (!disease && inc1 === 'yes' && inc2 === 'yes' && inc3 === 'yes') {
            const eligYes = document.getElementById('f1_eligible_yes');
            if (eligYes) eligYes.checked = false;
            if (badge) {
                badge.className = 'badge-calc badge-delay';
                badge.textContent = '⚠️ ข้อ 4: บังคับเลือก 1 ใน 3 กลุ่มโรค';
            }
        }
        scheduleAutoSave();
    }

    function toggleCciDm() {
        const chk = document.getElementById('f1_cci_dm_chk')?.checked;
        const rad1 = document.querySelector('input[name="f1_cci_dm_type"][value="1"]');
        if (chk && !document.querySelector('input[name="f1_cci_dm_type"]:checked')) {
            if (rad1) rad1.checked = true;
        } else if (!chk) {
            document.querySelectorAll('input[name="f1_cci_dm_type"]').forEach(r => r.checked = false);
        }
    }

    function toggleCciLiver() {
        const chk = document.getElementById('f1_cci_liver_chk')?.checked;
        const rad1 = document.querySelector('input[name="f1_cci_liver_type"][value="1"]');
        if (chk && !document.querySelector('input[name="f1_cci_liver_type"]:checked')) {
            if (rad1) rad1.checked = true;
        } else if (!chk) {
            document.querySelectorAll('input[name="f1_cci_liver_type"]').forEach(r => r.checked = false);
        }
    }

    function toggleCciTumor() {
        const chk = document.getElementById('f1_cci_tumor_chk')?.checked;
        const rad2 = document.querySelector('input[name="f1_cci_tumor_type"][value="2"]');
        if (chk && !document.querySelector('input[name="f1_cci_tumor_type"]:checked')) {
            if (rad2) rad2.checked = true;
        } else if (!chk) {
            document.querySelectorAll('input[name="f1_cci_tumor_type"]').forEach(r => r.checked = false);
        }
    }

    function calcCCI() {
        const ageVal = parseInt(document.getElementById('f1_age')?.value, 10);
        let agePoints = 0;
        if (!isNaN(ageVal)) {
            if (ageVal < 50) agePoints = 0;
            else if (ageVal <= 59) agePoints = 1;
            else if (ageVal <= 69) agePoints = 2;
            else if (ageVal <= 79) agePoints = 3;
            else if (ageVal >= 80) agePoints = 4;
        }

        const badge = document.getElementById('f1_age_score_badge');
        if (badge) badge.textContent = '+' + agePoints + ' คะแนน';

        let comorbPoints = 0;

        // DM
        if (document.getElementById('f1_cci_dm_chk')?.checked) {
            const dmType = document.querySelector('input[name="f1_cci_dm_type"]:checked')?.value;
            comorbPoints += (dmType === '2') ? 2 : 1;
        }
        // Liver
        if (document.getElementById('f1_cci_liver_chk')?.checked) {
            const livType = document.querySelector('input[name="f1_cci_liver_type"]:checked')?.value;
            comorbPoints += (livType === '3') ? 3 : 1;
        }
        // Tumor
        if (document.getElementById('f1_cci_tumor_chk')?.checked) {
            const tumType = document.querySelector('input[name="f1_cci_tumor_type"]:checked')?.value;
            comorbPoints += (tumType === '6') ? 6 : 2;
        }

        // Single Checkboxes (+1)
        if (document.getElementById('f1_cci_mi')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_chf')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_pvd')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_stroke')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_dementia')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_copd')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_ctd')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_pud')?.checked) comorbPoints += 1;

        // Single Checkboxes (+2)
        if (document.getElementById('f1_cci_hemi')?.checked) comorbPoints += 2;
        if (document.getElementById('f1_cci_ckd')?.checked) comorbPoints += 2;
        if (document.getElementById('f1_cci_leukemia')?.checked) comorbPoints += 2;
        if (document.getElementById('f1_cci_lymphoma')?.checked) comorbPoints += 2;

        // Single Checkboxes (+6)
        if (document.getElementById('f1_cci_aids')?.checked) comorbPoints += 6;

        const totalCCI = comorbPoints + agePoints;
        const totalEl = document.getElementById('f1_cci_total');
        if (totalEl) totalEl.value = totalCCI;

        const cPointEl = document.getElementById('f1_cci_comorb_points');
        if (cPointEl) cPointEl.textContent = comorbPoints;
        const aPointEl = document.getElementById('f1_cci_age_points');
        if (aPointEl) aPointEl.textContent = agePoints;

        scheduleAutoSave();
    }

    function calcVitals() {
        const sbp = parseFloat(document.getElementById('f1_sbp')?.value);
        const dbp = parseFloat(document.getElementById('f1_dbp')?.value);
        const hr = parseFloat(document.getElementById('f1_hr')?.value);

        let map = null;
        if (!isNaN(sbp) && !isNaN(dbp)) {
            map = Math.round(((sbp + 2 * dbp) / 3) * 10) / 10;
            document.getElementById('f1_map').value = map;
        } else {
            document.getElementById('f1_map').value = '';
        }

        const isStemi = document.getElementById('f1_inc4_stemi')?.checked;
        if (isStemi && map && !isNaN(hr)) {
            const msi = Math.round((hr / map) * 100) / 100;
            document.getElementById('f1_msi').value = msi.toFixed(2);
        } else {
            document.getElementById('f1_msi').value = '';
        }

        calcRTS();
        calcDeltaVitals();
        scheduleAutoSave();
    }

    function calcGCS() {
        const e = parseInt(document.getElementById('f1_gcs_e')?.value, 10);
        const v = parseInt(document.getElementById('f1_gcs_v')?.value, 10);
        const m = parseInt(document.getElementById('f1_gcs_m')?.value, 10);

        if (!isNaN(e) && !isNaN(v) && !isNaN(m)) {
            const total = e + v + m;
            document.getElementById('f1_gcs_total').value = total;

            const isStroke = document.getElementById('f1_inc4_ais')?.checked;
            if (isStroke) {
                // Auto-check Stroke Consciousness ONLY if disease is Stroke
                if (total >= 3 && total <= 8) {
                    const r1 = document.getElementById('f1_stroke_gcs_1'); if (r1) r1.checked = true;
                } else if (total >= 9 && total <= 12) {
                    const r2 = document.getElementById('f1_stroke_gcs_2'); if (r2) r2.checked = true;
                } else if (total >= 13 && total <= 15) {
                    const r3 = document.getElementById('f1_stroke_gcs_3'); if (r3) r3.checked = true;
                }
            } else {
                const r1 = document.getElementById('f1_stroke_gcs_1'); if (r1) r1.checked = false;
                const r2 = document.getElementById('f1_stroke_gcs_2'); if (r2) r2.checked = false;
                const r3 = document.getElementById('f1_stroke_gcs_3'); if (r3) r3.checked = false;
            }
        } else {
            document.getElementById('f1_gcs_total').value = '';
        }

        calcRTS();
        calcDeltaGCS();
        scheduleAutoSave();
    }

    function calcRTS() {
        const isTrauma = document.getElementById('f1_inc4_trauma')?.checked;
        if (!isTrauma) {
            // Cross-disease calculation prevention: RTS ONLY calculated for Severe Trauma (NOT for Stroke or STEMI)
            const rtsEl = document.getElementById('f1_rts_total');
            if (rtsEl) rtsEl.value = '';
            const crit = document.getElementById('f1_trauma_acuity_crit'); if (crit) crit.checked = false;
            const mod = document.getElementById('f1_trauma_acuity_mod'); if (mod) mod.checked = false;
            calcDeltaRTS();
            return;
        }

        const gcs = parseInt(document.getElementById('f1_gcs_total')?.value, 10);
        const sbp = parseFloat(document.getElementById('f1_sbp')?.value);
        const rr = parseFloat(document.getElementById('f1_rr')?.value);

        if (isNaN(gcs) || isNaN(sbp) || isNaN(rr)) {
            document.getElementById('f1_rts_total').value = '';
            calcDeltaRTS();
            return;
        }

        let cGCS = (gcs >= 13) ? 4 : (gcs >= 9 ? 3 : (gcs >= 6 ? 2 : (gcs >= 4 ? 1 : 0)));
        let cSBP = (sbp > 89) ? 4 : (sbp >= 76 ? 3 : (sbp >= 50 ? 2 : (sbp >= 1 ? 1 : 0)));
        let cRR = (rr >= 10 && rr <= 29) ? 4 : (rr > 29 ? 3 : (rr >= 6 ? 2 : (rr >= 1 ? 1 : 0)));

        const rts = Math.round((0.9368 * cGCS + 0.7326 * cSBP + 0.2908 * cRR) * 1000) / 1000;
        document.getElementById('f1_rts_total').value = rts.toFixed(3);

        if (rts <= 6.0) {
            const crit = document.getElementById('f1_trauma_acuity_crit');
            if (crit) crit.checked = true;
        } else {
            const mod = document.getElementById('f1_trauma_acuity_mod');
            if (mod) mod.checked = true;
        }

        calcDeltaRTS();
        scheduleAutoSave();
    }

    function calcTimelines() {
        autoDetectShift();

        // Form 1 Onset to ER
        const oDate = document.getElementById('f1_onset_date')?.value;
        const oTime = document.getElementById('f1_onset_time')?.value;
        const t0Date = document.getElementById('f1_t0_date')?.value;
        const t0Time = document.getElementById('f1_t0_time')?.value;

        if (oTime && t0Time) {
            const diff = diffMinutes(oDate, oTime, t0Date, t0Time);
            if (diff !== null && diff >= 0) {
                document.getElementById('f1_onset_to_er').value = diff;
            } else if (diff !== null && diff < 0) {
                document.getElementById('f1_onset_to_er').value = 'เวลาไม่ถูกต้อง';
            }
        } else {
            const oEl = document.getElementById('f1_onset_to_er');
            if (oEl) oEl.value = '';
        }

        // Form 1 DIDO (T0 to T1)
        let t1Date = document.getElementById('f1_t1_date')?.value;
        const t1Time = document.getElementById('f1_t1_time')?.value;

        // Auto cross-fill T1 date from T0 date if user omitted it
        if (!t1Date && t0Date && t1Time) {
            t1Date = t0Date;
            const f1_t1_d = document.getElementById('f1_t1_date');
            if (f1_t1_d) f1_t1_d.value = t0Date;
            const f2_t1_d = document.getElementById('f2_t1_date');
            if (f2_t1_d) f2_t1_d.value = t0Date;
        }

        const isTrauma = document.getElementById('f1_inc4_trauma')?.checked;
        const limit = isTrauma ? 60 : 45;

        if (t0Time && t1Time) {
            const dido = diffMinutes(t0Date, t0Time, t1Date, t1Time);
            setTimelineResult('f1_dido_min', 'f1_dido_ontime', 'f1_dido_delay', dido, limit);
            setTimelineResult('f2_t0_1_min', 'f2_dido_ontime', 'f2_dido_delay', dido, limit);
        } else {
            setTimelineResult('f1_dido_min', 'f1_dido_ontime', 'f1_dido_delay', null, limit);
            setTimelineResult('f2_t0_1_min', 'f2_dido_ontime', 'f2_dido_delay', null, limit);
        }

        calcForm2Timelines();
        calcForm3();
        calcForm4Timelines();
        scheduleAutoSave();
    }

    // --- FORM 2 CALCULATIONS ---
    function calcForm2Timelines() {
        const t0Date = document.getElementById('f2_t0_date')?.value;
        const t0Time = document.getElementById('f2_t0_time')?.value;
        const t1Date = document.getElementById('f2_t1_date')?.value;
        const t1Time = document.getElementById('f2_t1_time')?.value;
        const t2Date = document.getElementById('f2_t2_date')?.value;
        const t2Time = document.getElementById('f2_t2_time')?.value;
        const t3EmbarkDate = document.getElementById('f2_t3_embark_date')?.value;
        const t3EmbarkTime = document.getElementById('f2_t3_embark_time')?.value;
        const t3DisembarkDate = document.getElementById('f2_t3_disembark_date')?.value;
        const t3DisembarkTime = document.getElementById('f2_t3_disembark_time')?.value;
        const t4Date = document.getElementById('f2_t4_date')?.value;
        const t4Time = document.getElementById('f2_t4_time')?.value;
        const t5Date = document.getElementById('f2_t5_date')?.value;
        const t5Time = document.getElementById('f2_t5_time')?.value;

        // Auto sync T3 to Form 3
        if (t3EmbarkDate && document.getElementById('f3_t3_date')) {
            document.getElementById('f3_t3_date').value = t3EmbarkDate;
        }
        if (t3EmbarkTime && document.getElementById('f3_t3_time')) {
            document.getElementById('f3_t3_time').value = t3EmbarkTime;
        }

        const isTrauma = document.getElementById('f1_inc4_trauma')?.checked;
        const isStroke = document.getElementById('f1_inc4_ais')?.checked;

        // T0-1 Island DIDO
        if (t0Time && t1Time) {
            const dido = diffMinutes(t0Date, t0Time, t1Date, t1Time);
            setTimelineResult('f2_t0_1_min', 'f2_dido_ontime', 'f2_dido_delay', dido, isTrauma ? 60 : 45);
        } else {
            setTimelineResult('f2_t0_1_min', 'f2_dido_ontime', 'f2_dido_delay', null, 45);
        }

        // T2 Island Road (T1 to T2)
        if (t1Time && t2Time) {
            const road = diffMinutes(t1Date, t1Time, t2Date, t2Time);
            setTimelineResult('f2_t2_min', 'f2_road_ontime', 'f2_road_delay', road, 12);
        } else {
            setTimelineResult('f2_t2_min', 'f2_road_ontime', 'f2_road_delay', null, 12);
        }

        // Waiting at Pier (T2 to T3 embark)
        if (t2Time && t3EmbarkTime) {
            const wait = diffMinutes(t2Date, t2Time, t3EmbarkDate, t3EmbarkTime);
            setTimelineResult('f2_t_wait_min', 'f2_wait_ontime', 'f2_wait_delay', wait, 5);
        } else {
            setTimelineResult('f2_t_wait_min', 'f2_wait_ontime', 'f2_wait_delay', null, 5);
        }

        // T3 Water Crossing
        if (t3DisembarkTime && (t3EmbarkTime || t2Time)) {
            const startT = t3EmbarkTime || t2Time;
            const startD = t3EmbarkTime ? t3EmbarkDate : t2Date;
            const water = diffMinutes(startD, startT, t3DisembarkDate, t3DisembarkTime);
            setTimelineResult('f2_t3_min', 'f2_water_ontime', 'f2_water_delay', water, 24);
        } else {
            setTimelineResult('f2_t3_min', 'f2_water_ontime', 'f2_water_delay', null, 24);
        }

        // T4 Mainland Highway
        if (t3DisembarkTime && t4Time) {
            const hwy = diffMinutes(t3DisembarkDate, t3DisembarkTime, t4Date, t4Time);
            setTimelineResult('f2_t4_min', 'f2_hwy_ontime', 'f2_hwy_delay', hwy, 60);
        } else {
            setTimelineResult('f2_t4_min', 'f2_hwy_ontime', 'f2_hwy_delay', null, 60);
        }

        // T_Total System Time
        if (t0Time && t4Time) {
            const total = diffMinutes(t0Date, t0Time, t4Date, t4Time);
            setTimelineResult('f2_t_total_min', 'f2_total_ontime', 'f2_total_delay', total, isTrauma ? 156 : 141);
        } else {
            setTimelineResult('f2_t_total_min', 'f2_total_ontime', 'f2_total_delay', null, 141);
        }

        // T5 Definitive Management
        if (t0Time && t5Time) {
            const t5 = diffMinutes(t0Date, t0Time, t5Date, t5Time);
            setTimelineResult('f2_t5_min', 'f2_t5_ontime', 'f2_t5_delay', t5, isStroke ? 156 : 180);
        } else {
            setTimelineResult('f2_t5_min', 'f2_t5_ontime', 'f2_t5_delay', null, 180);
        }

        calcForm3();
        autoDetectFerryOperate();
        if (typeof updateEpidemiologicalAssessment === 'function') updateEpidemiologicalAssessment();
        scheduleAutoSave();
    }

    function calcCompositeAE() {
        toggleCprDetails();
        const cpr = document.querySelector('input[name="f2_ae_cpr"]:checked')?.value === '1';
        const intub = document.querySelector('input[name="f2_ae_intub"]:checked')?.value === '1';
        const inotropes = document.querySelector('input[name="f2_ae_inotropes"]:checked')?.value === '1';
        const dislodge = document.querySelector('input[name="f2_ae_dislodge"]:checked')?.value === '1';
        const death = document.querySelector('input[name="f2_ae_death"]:checked')?.value === '1';

        const isEvent = (cpr || intub || inotropes || dislodge || death);
        if (isEvent) {
            document.getElementById('f2_comp_event').checked = true;
        } else {
            document.getElementById('f2_comp_stable').checked = true;
        }

        calcCompositeDeterioration();
        scheduleAutoSave();
    }

    // --- FORM 3 CALCULATIONS ---
    function updateTidePhaseBadgeManual() {
        const curPhase = document.querySelector('input[name="f3_tide_phase"]:checked')?.value;
        const badgePhase = document.getElementById('f3_tide_phase_badge');
        if (!badgePhase) return;
        if (curPhase === '1') {
            badgePhase.innerHTML = '<span style="color:#0369a1; font-size:11px;">(เลือกระยะน้ำ: 1 = น้ำขึ้น Flood Tide)</span>';
        } else if (curPhase === '2') {
            badgePhase.innerHTML = '<span style="color:#b91c1c; font-size:11px;">(เลือกระยะน้ำ: 2 = น้ำลง Ebb Tide)</span>';
        } else if (curPhase === '3') {
            badgePhase.innerHTML = '<span style="color:#475569; font-size:11px;">(เลือกระยะน้ำ: 3 = น้ำนิ่ง/น้ำทรง Slack Water)</span>';
        }
        if (typeof updateEpidemiologicalAssessment === 'function') updateEpidemiologicalAssessment();
        scheduleAutoSave();
    }

    function calcTide() {
        const h = parseFloat(document.getElementById('f3_tide_height')?.value);
        const badgePhase = document.getElementById('f3_tide_phase_badge');

        if (!isNaN(h)) {
            // 1. TIDE_EXTREME_LOW (< 1.0 m LAT)
            if (h < 1.0) {
                const low = document.getElementById('f3_tide_low');
                if (low) low.checked = true;
            } else {
                const norm = document.getElementById('f3_tide_normal');
                if (norm) norm.checked = true;
            }

            // 2. Auto TIDE_PHASE selection based on TIDE_HEIGHT_M
            const floodRad = document.getElementById('f3_tide_phase_flood');
            const ebbRad = document.getElementById('f3_tide_phase_ebb');

            if (h < 1.0) {
                if (ebbRad) ebbRad.checked = true;
                if (badgePhase) {
                    badgePhase.innerHTML = `<span style="display:inline-flex; align-items:center; gap:4px; background:#fee2e2; color:#991b1b; padding:2px 8px; border-radius:10px; font-weight:600; font-size:11px;">⚡ Auto: 2 = น้ำลง (Ebb Tide) จากระดับน้ำ ${h.toFixed(2)} ม. (&lt; 1.0 ม.)</span>`;
                }
            } else {
                if (floodRad) floodRad.checked = true;
                if (badgePhase) {
                    badgePhase.innerHTML = `<span style="display:inline-flex; align-items:center; gap:4px; background:#e0f2fe; color:#0369a1; padding:2px 8px; border-radius:10px; font-weight:600; font-size:11px;">⚡ Auto: 1 = น้ำขึ้น (Flood Tide) จากระดับน้ำ ${h.toFixed(2)} ม. (&ge; 1.0 ม.)</span>`;
                }
            }
        } else {
            if (badgePhase) badgePhase.innerHTML = '';
        }
        if (typeof updateEpidemiologicalAssessment === 'function') updateEpidemiologicalAssessment();
        scheduleAutoSave();
    }

    function toggleRainDetails() {
        const precipVal = document.querySelector('input[name="f3_precipitation"]:checked')?.value;
        const rainInput = document.getElementById('f3_rainfall_mm');
        const rainNormRad = document.getElementById('f3_rain_normal');
        const rainHeavyRad = document.getElementById('f3_rain_heavy');
        const rowRain = document.getElementById('row_f3_rainfall');
        const rowTorr = document.getElementById('row_f3_torrential');
        const rainHint = document.getElementById('f3_rain_hint');

        if (precipVal === '0') {
            // สภาพฝนตกขณะส่งต่อ = 0 (ไม่มีฝน / อากาศแจ่มใส): ไม่ต้องทำปริมาณฝนและเกณฑ์พายุ
            if (rainInput) {
                rainInput.disabled = true;
                rainInput.value = '';
                rainInput.style.backgroundColor = '#f1f5f9';
                rainInput.style.color = '#94a3b8';
            }
            if (rainNormRad) {
                rainNormRad.checked = true;
                rainNormRad.disabled = true;
            }
            if (rainHeavyRad) {
                rainHeavyRad.checked = false;
                rainHeavyRad.disabled = true;
            }
            if (rowRain) {
                rowRain.style.opacity = '0.45';
                rowRain.style.backgroundColor = '#f8fafc';
            }
            if (rowTorr) {
                rowTorr.style.opacity = '0.45';
                rowTorr.style.backgroundColor = '#f8fafc';
            }
            if (rainHint) {
                rainHint.innerHTML = '<span style="color: #15803d; font-weight: 600;">✓ ไม่ต้องกรอก (สภาพฝนตกขณะส่งต่อ = 0 ไม่มีฝน)</span>';
            }
        } else if (precipVal === '1') {
            // สภาพฝนตกขณะส่งต่อ = 1 (ฝนตกหนัก / พายุ): ให้กรอก
            if (rainInput) {
                rainInput.disabled = false;
                rainInput.style.backgroundColor = '#ffffff';
                rainInput.style.color = '';
            }
            if (rainNormRad) rainNormRad.disabled = false;
            if (rainHeavyRad) rainHeavyRad.disabled = false;
            if (rowRain) {
                rowRain.style.opacity = '1';
                rowRain.style.backgroundColor = '';
            }
            if (rowTorr) {
                rowTorr.style.opacity = '1';
                rowTorr.style.backgroundColor = '';
            }
            if (rainHint) {
                rainHint.innerHTML = '<span style="color: #b45309; font-weight: 600;">⚠️ ฝนตกขณะส่งต่อ: ระบุปริมาณฝนสะสมเพื่อประเมินเกณฑ์พายุ</span>';
            }
            calcRain();
        } else {
            if (rainInput) {
                rainInput.disabled = false;
                rainInput.style.backgroundColor = '#ffffff';
                rainInput.style.color = '';
            }
            if (rainNormRad) rainNormRad.disabled = false;
            if (rainHeavyRad) rainHeavyRad.disabled = false;
            if (rowRain) {
                rowRain.style.opacity = '1';
                rowRain.style.backgroundColor = '';
            }
            if (rowTorr) {
                rowTorr.style.opacity = '1';
                rowTorr.style.backgroundColor = '';
            }
            if (rainHint) rainHint.innerHTML = '';
        }
        if (typeof updateEpidemiologicalAssessment === 'function') updateEpidemiologicalAssessment();
        scheduleAutoSave();
    }

    function calcRain() {
        const r = parseFloat(document.getElementById('f3_rainfall_mm')?.value);
        if (!isNaN(r)) {
            if (r >= 10.0) {
                const heavy = document.getElementById('f3_rain_heavy');
                if (heavy) heavy.checked = true;
            } else {
                const norm = document.getElementById('f3_rain_normal');
                if (norm) norm.checked = true;
            }
        }
        if (typeof updateEpidemiologicalAssessment === 'function') updateEpidemiologicalAssessment();
        scheduleAutoSave();
    }

    function calcForm3() {
        // Season auto-evaluation
        const t3Date = document.getElementById('f3_t3_date')?.value || document.getElementById('f2_t3_embark_date')?.value || document.getElementById('f1_t0_date')?.value;
        if (t3Date) {
            const parts = t3Date.split('-');
            if (parts.length >= 2) {
                const m = parseInt(parts[1], 10);
                if (m >= 5 && m <= 10) {
                    const mon = document.getElementById('f3_season_monsoon');
                    if (mon) mon.checked = true;
                } else if (m >= 1 && m <= 12) {
                    const dry = document.getElementById('f3_season_dry');
                    if (dry) dry.checked = true;
                }
            }
        }

        // Auto sync ED shift based on T1 (from autoDetectShift)
        autoDetectShift();

        calcTide();
        toggleRainDetails();
        if (typeof updateEpidemiologicalAssessment === 'function') updateEpidemiologicalAssessment();
        scheduleAutoSave();
    }

    // --- FORM 4 CALCULATIONS ---
    function calcKrabiVitals() {
        const sbp = parseFloat(document.getElementById('f4_sbp')?.value);
        const dbp = parseFloat(document.getElementById('f4_dbp')?.value);
        const hr = parseFloat(document.getElementById('f4_hr')?.value);

        let map = null;
        if (!isNaN(sbp) && !isNaN(dbp)) {
            map = Math.round(((sbp + 2 * dbp) / 3) * 10) / 10;
            document.getElementById('f4_map').value = map;
        } else {
            document.getElementById('f4_map').value = '';
        }

        const isStemi = document.getElementById('f1_inc4_stemi')?.checked;
        if (isStemi && map && !isNaN(hr)) {
            const msi = Math.round((hr / map) * 100) / 100;
            document.getElementById('f4_msi').value = msi.toFixed(2);
        } else {
            document.getElementById('f4_msi').value = '';
        }

        calcDeltaVitals();
        calcDeltaRTS();
        scheduleAutoSave();
    }

    function calcKrabiGCS() {
        const e = parseInt(document.getElementById('f4_gcs_e')?.value, 10);
        const v = parseInt(document.getElementById('f4_gcs_v')?.value, 10);
        const m = parseInt(document.getElementById('f4_gcs_m')?.value, 10);

        if (!isNaN(e) && !isNaN(v) && !isNaN(m)) {
            const total = e + v + m;
            document.getElementById('f4_gcs_total').value = total;

            const isStroke = document.getElementById('f1_inc4_ais')?.checked;
            if (isStroke) {
                // Auto-check Stroke Consciousness in Form 4 if disease is Stroke
                if (total >= 3 && total <= 8) {
                    const r1 = document.getElementById('f4_stroke_gcs_1'); if (r1) r1.checked = true;
                } else if (total >= 9 && total <= 12) {
                    const r2 = document.getElementById('f4_stroke_gcs_2'); if (r2) r2.checked = true;
                } else if (total >= 13 && total <= 15) {
                    const r3 = document.getElementById('f4_stroke_gcs_3'); if (r3) r3.checked = true;
                }
            }
        } else {
            const curTot = parseInt(document.getElementById('f4_gcs_total')?.value, 10);
            if (isNaN(curTot)) document.getElementById('f4_gcs_total').value = '';
        }

        calcDeltaGCS();
        calcDeltaRTS();
        scheduleAutoSave();
    }

    function calcDeltaKillip() {
        const isStemi = document.getElementById('f1_inc4_stemi')?.checked;
        if (!isStemi) {
            const fFrom = document.getElementById('f4_delta_killip_from'); if (fFrom) fFrom.value = '';
            const fTo = document.getElementById('f4_delta_killip_to'); if (fTo) fTo.value = '';
            const k1 = document.getElementById('f4_killip_deter'); if (k1) k1.checked = false;
            const k2 = document.getElementById('f4_killip_stable'); if (k2) k2.checked = false;
            calcCompositeDeterioration();
            return;
        }

        const lantaKillip = document.querySelector('input[name="f1_killip"]:checked')?.value;
        const krabiKillip = document.querySelector('input[name="f4_killip"]:checked')?.value;

        if (lantaKillip) document.getElementById('f4_delta_killip_from').value = lantaKillip;
        if (krabiKillip) document.getElementById('f4_delta_killip_to').value = krabiKillip;

        if (lantaKillip && krabiKillip) {
            let kVal = 1;
            if (krabiKillip === '1_2') kVal = 1.5;
            else if (krabiKillip === '3') kVal = 3;
            else if (krabiKillip === '4') kVal = 4;

            const lVal = parseFloat(lantaKillip);
            const diff = kVal - lVal;

            if (diff >= 1 || krabiKillip === '4') {
                document.getElementById('f4_killip_deter').checked = true;
            } else {
                document.getElementById('f4_killip_stable').checked = true;
            }
        } else {
            const k1 = document.getElementById('f4_killip_deter'); if (k1) k1.checked = false;
            const k2 = document.getElementById('f4_killip_stable'); if (k2) k2.checked = false;
        }
        calcCompositeDeterioration();
        scheduleAutoSave();
    }

    function calcDeltaGCS() {
        const lGCS = parseInt(document.getElementById('f1_gcs_total')?.value, 10);
        const kGCS = parseInt(document.getElementById('f4_gcs_total')?.value || document.getElementById('f2_mon4_gcs')?.value, 10);
        
        if (!isNaN(lGCS) && !isNaN(kGCS)) {
            const diff = kGCS - lGCS;
            document.getElementById('f4_delta_gcs').value = (diff > 0 ? '+' : '') + diff;
            if (diff <= -2) {
                document.getElementById('f4_gcs_deter').checked = true;
                const gStab = document.getElementById('f4_gcs_stable'); if (gStab) gStab.checked = false;
            } else {
                document.getElementById('f4_gcs_stable').checked = true;
                const gDet = document.getElementById('f4_gcs_deter'); if (gDet) gDet.checked = false;
            }
        } else {
            const deltaGcsEl = document.getElementById('f4_delta_gcs'); if (deltaGcsEl) deltaGcsEl.value = '';
            const g1 = document.getElementById('f4_gcs_deter'); if (g1) g1.checked = false;
            const g2 = document.getElementById('f4_gcs_stable'); if (g2) g2.checked = false;
        }
        calcCompositeDeterioration();
    }

    function calcDeltaRTS() {
        const isTrauma = document.getElementById('f1_inc4_trauma')?.checked;
        if (!isTrauma) {
            const deltaRtsEl = document.getElementById('f4_delta_rts'); if (deltaRtsEl) deltaRtsEl.value = '';
            const d1 = document.getElementById('f4_rts_deter'); if (d1) d1.checked = false;
            const d2 = document.getElementById('f4_rts_stable'); if (d2) d2.checked = false;
            const f4Crit = document.getElementById('f4_trauma_crit'); if (f4Crit) f4Crit.checked = false;
            const f4Mod = document.getElementById('f4_trauma_mod'); if (f4Mod) f4Mod.checked = false;
            calcCompositeDeterioration();
            return;
        }

        const lRTS = parseFloat(document.getElementById('f1_rts_total')?.value);
        const kSBP = parseFloat(document.getElementById('f4_sbp')?.value);
        const kRR = parseFloat(document.getElementById('f4_rr')?.value);
        const kGCS = parseInt(document.getElementById('f4_gcs_total')?.value || document.getElementById('f2_mon4_gcs')?.value || document.getElementById('f1_gcs_total')?.value, 10);

        if (!isNaN(lRTS) && !isNaN(kSBP) && !isNaN(kRR) && !isNaN(kGCS)) {
            let cGCS = (kGCS >= 13) ? 4 : (kGCS >= 9 ? 3 : (kGCS >= 6 ? 2 : (kGCS >= 4 ? 1 : 0)));
            let cSBP = (kSBP > 89) ? 4 : (kSBP >= 76 ? 3 : (kSBP >= 50 ? 2 : (kSBP >= 1 ? 1 : 0)));
            let cRR = (kRR >= 10 && kRR <= 29) ? 4 : (kRR > 29 ? 3 : (kRR >= 6 ? 2 : (kRR >= 1 ? 1 : 0)));
            const kRTS = Math.round((0.9368 * cGCS + 0.7326 * cSBP + 0.2908 * cRR) * 1000) / 1000;

            const diff = Math.round((kRTS - lRTS) * 1000) / 1000;
            document.getElementById('f4_delta_rts').value = (diff > 0 ? '+' : '') + diff.toFixed(3);

            if (diff <= -1.0) {
                document.getElementById('f4_rts_deter').checked = true;
                const rStab = document.getElementById('f4_rts_stable'); if (rStab) rStab.checked = false;
            } else {
                document.getElementById('f4_rts_stable').checked = true;
                const rDet = document.getElementById('f4_rts_deter'); if (rDet) rDet.checked = false;
            }

            if (kRTS <= 6.0) {
                const f4Crit = document.getElementById('f4_trauma_crit'); if (f4Crit) f4Crit.checked = true;
                const f4Mod = document.getElementById('f4_trauma_mod'); if (f4Mod) f4Mod.checked = false;
            } else {
                const f4Mod = document.getElementById('f4_trauma_mod'); if (f4Mod) f4Mod.checked = true;
                const f4Crit = document.getElementById('f4_trauma_crit'); if (f4Crit) f4Crit.checked = false;
            }
        } else {
            const deltaRtsEl = document.getElementById('f4_delta_rts'); if (deltaRtsEl) deltaRtsEl.value = '';
            const d1 = document.getElementById('f4_rts_deter'); if (d1) d1.checked = false;
            const d2 = document.getElementById('f4_rts_stable'); if (d2) d2.checked = false;
        }
        calcCompositeDeterioration();
    }

    function calcDeltaVitals() {
        // MAP Delta
        // Rule: if MAP drops (diffMAP < 0) but Krabi MAP is still >= 65 mmHg, evaluate as stable (adequate perfusion)
        // Only evaluate as deteriorated if diffMAP < 0 AND Krabi MAP < 65 mmHg
        const lMAP = parseFloat(document.getElementById('f1_map')?.value);
        const kMAP = parseFloat(document.getElementById('f4_map')?.value);
        if (!isNaN(lMAP) && !isNaN(kMAP)) {
            const diffMAP = Math.round((kMAP - lMAP) * 10) / 10;
            document.getElementById('f4_delta_map').value = (diffMAP > 0 ? '+' : '') + diffMAP;
            if (diffMAP < 0 && kMAP < 65) {
                document.getElementById('f4_map_deter').checked = true;
                const mStab = document.getElementById('f4_map_stable'); if (mStab) mStab.checked = false;
            } else {
                document.getElementById('f4_map_stable').checked = true;
                const mDet = document.getElementById('f4_map_deter'); if (mDet) mDet.checked = false;
            }
        } else {
            const dMapEl = document.getElementById('f4_delta_map'); if (dMapEl) dMapEl.value = '';
            const d1 = document.getElementById('f4_map_deter'); if (d1) d1.checked = false;
            const d2 = document.getElementById('f4_map_stable'); if (d2) d2.checked = false;
        }

        // MSI Delta - ONLY for STEMI
        const isStemi = document.getElementById('f1_inc4_stemi')?.checked;
        const lMSI = parseFloat(document.getElementById('f1_msi')?.value);
        const kMSI = parseFloat(document.getElementById('f4_msi')?.value);
        if (isStemi && !isNaN(lMSI) && !isNaN(kMSI)) {
            const diffMSI = Math.round((kMSI - lMSI) * 100) / 100;
            document.getElementById('f4_delta_msi').value = (diffMSI > 0 ? '+' : '') + diffMSI.toFixed(2);
            if (diffMSI >= 0.15) {
                document.getElementById('f4_msi_deter').checked = true;
                const mStab = document.getElementById('f4_msi_stable'); if (mStab) mStab.checked = false;
            } else {
                document.getElementById('f4_msi_stable').checked = true;
                const mDet = document.getElementById('f4_msi_deter'); if (mDet) mDet.checked = false;
            }
        } else {
            const dMsi = document.getElementById('f4_delta_msi'); if (dMsi) dMsi.value = '';
            const m1 = document.getElementById('f4_msi_deter'); if (m1) m1.checked = false;
            const m2 = document.getElementById('f4_msi_stable'); if (m2) m2.checked = false;
        }

        calcCompositeDeterioration();
    }

    function calcDeltaBT() {
        const lBT = parseFloat(document.getElementById('f1_bt')?.value);
        const kBT = parseFloat(document.getElementById('f4_bt')?.value);
        if (!isNaN(lBT) && !isNaN(kBT)) {
            const diffBT = Math.round((kBT - lBT) * 10) / 10;
            document.getElementById('f4_delta_bt').value = (diffBT > 0 ? '+' : '') + diffBT;
            if (kBT < 35.0) {
                document.getElementById('f4_bt_hypo').checked = true;
                const bNorm = document.getElementById('f4_bt_normal'); if (bNorm) bNorm.checked = false;
            } else {
                document.getElementById('f4_bt_normal').checked = true;
                const bHypo = document.getElementById('f4_bt_hypo'); if (bHypo) bHypo.checked = false;
            }
        }
        calcCompositeDeterioration();
    }

    function calcCompositeDeterioration() {
        const isStemi = document.getElementById('f1_inc4_stemi')?.checked;
        const isTrauma = document.getElementById('f1_inc4_trauma')?.checked;

        const kDeter = isStemi && document.getElementById('f4_killip_deter')?.checked;
        const rDeter = isTrauma && document.getElementById('f4_rts_deter')?.checked;
        const gDeter = document.getElementById('f4_gcs_deter')?.checked;
        const mDeter = isStemi && document.getElementById('f4_msi_deter')?.checked;
        const pDeter = document.getElementById('f4_map_deter')?.checked;
        const bDeter = document.getElementById('f4_bt_hypo')?.checked;
        const aeEvent = document.getElementById('f2_comp_event')?.checked;

        const isDeter = (kDeter || gDeter || rDeter || mDeter || pDeter || bDeter || aeEvent);
        if (isDeter) {
            document.getElementById('f4_deter_event').checked = true;
        } else {
            document.getElementById('f4_deter_stable').checked = true;
        }
        scheduleAutoSave();
    }

    function calcForm4Timelines() {
        let t4Date = document.getElementById('f4_t4_date')?.value || document.getElementById('f2_t4_date')?.value || document.getElementById('f1_t0_date')?.value;
        let t4Time = document.getElementById('f4_t4_time')?.value || document.getElementById('f2_t4_time')?.value;
        let t5Date = document.getElementById('f4_t5_date')?.value || document.getElementById('f2_t5_date')?.value || t4Date;
        let t5Time = document.getElementById('f4_t5_time')?.value || document.getElementById('f2_t5_time')?.value;

        // Auto sync to Form 4 inputs if empty
        const f4_t4_d = document.getElementById('f4_t4_date');
        const f4_t4_t = document.getElementById('f4_t4_time');
        const f4_t5_d = document.getElementById('f4_t5_date');
        const f4_t5_t = document.getElementById('f4_t5_time');
        if (f4_t4_d && !f4_t4_d.value && t4Date) f4_t4_d.value = t4Date;
        if (f4_t4_t && !f4_t4_t.value && t4Time) f4_t4_t.value = t4Time;
        if (f4_t5_d && !f4_t5_d.value && t5Date) f4_t5_d.value = t5Date;
        if (f4_t5_t && !f4_t5_t.value && t5Time) f4_t5_t.value = t5Time;

        const outEl = document.getElementById('f4_t4_5_min');
        if (outEl) {
            if (t4Time && t5Time) {
                const d2i = diffMinutes(t4Date, t4Time, t5Date, t5Time);
                outEl.value = (d2i !== null && !isNaN(d2i)) ? d2i : '--';
            } else {
                outEl.value = '';
            }
        }
        calcGoldenWindows();
        scheduleAutoSave();
    }

    function calcGoldenWindows() {
        const isStemi = document.getElementById('f1_inc4_stemi')?.checked;
        const isStroke = document.getElementById('f1_inc4_ais')?.checked;
        const isTrauma = document.getElementById('f1_inc4_trauma')?.checked;

        const t0Date = document.getElementById('f1_t0_date')?.value;
        const t0Time = document.getElementById('f1_t0_time')?.value;
        const oDate = document.getElementById('f1_onset_date')?.value;
        const oTime = document.getElementById('f1_onset_time')?.value;

        // 1. STEMI Door-to-Balloon
        if (isStemi) {
            const wireTime = document.getElementById('f4_pci_wire_time')?.value;
            const t5Date = document.getElementById('f4_t5_date')?.value || t0Date;
            if (t0Time && wireTime) {
                const d2b = diffMinutes(t0Date, t0Time, t5Date, wireTime);
                setTimelineResult('f4_pci_d2b_min', 'f4_pci_achieved', 'f4_pci_missed', d2b, 180);
            } else {
                setTimelineResult('f4_pci_d2b_min', 'f4_pci_achieved', 'f4_pci_missed', null, 180);
            }
        } else {
            setTimelineResult('f4_pci_d2b_min', 'f4_pci_achieved', 'f4_pci_missed', null, 180);
        }

        // 2. Stroke Onset to Needle
        if (isStroke) {
            const rtpaTime = document.getElementById('f4_rtpa_time')?.value;
            const t5Date = document.getElementById('f4_t5_date')?.value || t0Date;
            if (oTime && rtpaTime) {
                const o2n = diffMinutes(oDate, oTime, t5Date, rtpaTime);
                setTimelineResult('f4_stroke_o2n_min', 'f4_stroke_achieved', 'f4_stroke_missed', o2n, 270);
            } else {
                setTimelineResult('f4_stroke_o2n_min', 'f4_stroke_achieved', 'f4_stroke_missed', null, 270);
            }
        } else {
            setTimelineResult('f4_stroke_o2n_min', 'f4_stroke_achieved', 'f4_stroke_missed', null, 270);
        }

        // 3. Trauma Door to CT & Door to OR
        if (isTrauma) {
            const ctTime = document.getElementById('f4_trauma_ct_time')?.value;
            const orTime = document.getElementById('f4_or_time')?.value;
            const t5Date = document.getElementById('f4_t5_date')?.value || t0Date;

            let d2ct = null;
            let d2or = null;
            let isCtAchieved = null;
            let isOrAchieved = null;

            const d2ctEl = document.getElementById('f4_trauma_d2ct_min');
            const d2orEl = document.getElementById('f4_trauma_d2or_min');
            const achEl = document.getElementById('f4_trauma_achieved');
            const misEl = document.getElementById('f4_trauma_missed');

            if (t0Time && ctTime) {
                d2ct = diffMinutes(t0Date, t0Time, t5Date, ctTime);
                if (d2ctEl) d2ctEl.value = (d2ct !== null && d2ct >= 0) ? d2ct : (d2ct < 0 ? 'เวลาไม่ถูกต้อง' : '');
                if (d2ct !== null && d2ct >= 0) {
                    isCtAchieved = (d2ct <= 150);
                }
            } else {
                if (d2ctEl) d2ctEl.value = '';
            }

            if (t0Time && orTime) {
                d2or = diffMinutes(t0Date, t0Time, t5Date, orTime);
                if (d2orEl) d2orEl.value = (d2or !== null && d2or >= 0) ? d2or : (d2or < 0 ? 'เวลาไม่ถูกต้อง' : '');
                if (d2or !== null && d2or >= 0) {
                    isOrAchieved = (d2or <= 180);
                }
            } else {
                if (d2orEl) d2orEl.value = '';
            }

            // Evaluate Golden Window:
            if (isOrAchieved !== null && isCtAchieved !== null) {
                if (isOrAchieved && isCtAchieved) {
                    if (achEl) achEl.checked = true;
                    if (misEl) misEl.checked = false;
                } else if (!isOrAchieved || !isCtAchieved) {
                    if (misEl) misEl.checked = true;
                    if (achEl) achEl.checked = false;
                }
            } else if (isOrAchieved !== null) {
                if (isOrAchieved) {
                    if (achEl) achEl.checked = true;
                    if (misEl) misEl.checked = false;
                } else {
                    if (misEl) misEl.checked = true;
                    if (achEl) achEl.checked = false;
                }
            } else if (isCtAchieved !== null) {
                if (isCtAchieved) {
                    if (achEl) achEl.checked = true;
                    if (misEl) misEl.checked = false;
                } else {
                    if (misEl) misEl.checked = true;
                    if (achEl) achEl.checked = false;
                }
            } else {
                if (achEl) achEl.checked = false;
                if (misEl) misEl.checked = false;
            }

            // Auto-fill T5 time if empty (use earlier of CT or OR)
            const t5TimeInput = document.getElementById('f4_t5_time');
            if (t5TimeInput && !t5TimeInput.value) {
                const earliestTime = ctTime || orTime;
                if (earliestTime) {
                    t5TimeInput.value = earliestTime;
                    syncT5_fromF4();
                }
            }
        } else {
            const d2ctEl = document.getElementById('f4_trauma_d2ct_min');
            const d2orEl = document.getElementById('f4_trauma_d2or_min');
            const achEl = document.getElementById('f4_trauma_achieved');
            const misEl = document.getElementById('f4_trauma_missed');
            if (d2ctEl) d2ctEl.value = '';
            if (d2orEl) d2orEl.value = '';
            if (achEl) achEl.checked = false;
            if (misEl) misEl.checked = false;
        }
        if (typeof updateEpidemiologicalAssessment === 'function') updateEpidemiologicalAssessment();
    }

    // --- EPIDEMIOLOGICAL COHORT & MICRO-TIMELINE DELAY ASSESSMENT ENGINE ---
    function updateEpidemiologicalAssessment() {
        const cohortBadge = document.getElementById('cohort_badge_container');
        const cohortFactorsEl = document.getElementById('cohort_factors_container');
        const delayBadge = document.getElementById('delay_count_badge');
        const timelineSummary = document.getElementById('timeline_summary_badge');
        const timelineDelaysEl = document.getElementById('timeline_delays_container');

        if (!cohortBadge || !cohortFactorsEl || !timelineDelaysEl) return;

        // --- 1. COHORT EXPOSURE CLASSIFICATION ---
        const exposedFactors = [];

        // Determinant 1: Off-hour ferry (24:00-05:00)
        const ferryF2 = document.querySelector('input[name="f2_ferry_operate"]:checked')?.value;
        const ferryF3 = document.querySelector('input[name="f3_ferry_shift"]:checked')?.value;
        const t2Time = document.getElementById('f2_t2_time')?.value;
        const t3EmbarkTime = document.getElementById('f2_t3_embark_time')?.value;
        let isOffHour = (ferryF2 === '1' || ferryF3 === '1');
        if (!isOffHour && (t3EmbarkTime || t2Time)) {
            const ferryTime = t3EmbarkTime || t2Time;
            const parts = ferryTime.split(':');
            if (parts.length >= 2) {
                const h = parseInt(parts[0], 10);
                if (!isNaN(h) && (h >= 0 && h < 5)) isOffHour = true;
            }
        }
        if (isOffHour) {
            exposedFactors.push({
                name: 'การเดินแพนอกเวลาปกติ (Off-Hour Ferry: 24:00–05:00 น.)',
                desc: 'แพปิดบริการรอบปกติ ต้องโทรเรียกคนขับแพฉุกเฉิน (Emergency On-Call)',
                icon: '⛴️'
            });
        }

        // Determinant 2: Monsoon season (May-Oct)
        const season = document.querySelector('input[name="f3_season"]:checked')?.value;
        if (season === '0') {
            exposedFactors.push({
                name: 'ฤดูมรสุมตะวันตกเฉียงใต้ (Southwest Monsoon Season: พ.ค.–ต.ค.)',
                desc: 'สภาพอากาศ คลื่นลม และร่องน้ำทะเลอันดามันมีความแปรปรวนสูง',
                icon: '🌊'
            });
        }

        // Determinant 3: Low tide / Sandbar hazard
        const tideLow = document.querySelector('input[name="f3_tide_extreme"]:checked')?.value;
        const sandbar = document.querySelector('input[name="f3_sandbar_risk"]:checked')?.value;
        const tideH = parseFloat(document.getElementById('f3_tide_height')?.value);
        if (tideLow === '1' || sandbar === '1' || (!isNaN(tideH) && tideH < 1.0)) {
            exposedFactors.push({
                name: 'ภาวะน้ำลงต่ำสุดวิกฤต / สันดอนทรายตื้นเขิน (Extreme Low Tide / Sandbar)',
                desc: 'ระดับน้ำ < 1.0 ม. LAT หรือเสี่ยงติดสันทราย แพต้องเดินเรืออ้อมแนวร่องน้ำ',
                icon: '⚓'
            });
        }

        // Determinant 4: Rough sea state (> 2.0m / Beaufort >= 5)
        const seaState = document.querySelector('input[name="f3_sea_state"]:checked')?.value;
        const waveH = parseFloat(document.getElementById('f3_wave_height')?.value);
        if (seaState === '2' || (!isNaN(waveH) && waveH > 2.0)) {
            exposedFactors.push({
                name: 'คลื่นลมแรงในร่องน้ำทะเลอันดามัน (Rough Sea / High Waves > 2.0m)',
                desc: 'ความสูงคลื่น > 2.0 เมตร เพิ่มความโคลงเคลงและเวลาข้ามฟาก',
                icon: '💨'
            });
        }

        // Determinant 5: Torrential rain / Storm (>= 10.0 mm/hr)
        const rainPrecip = document.querySelector('input[name="f3_precipitation"]:checked')?.value;
        const rainHeavy = document.querySelector('input[name="f3_torrential_rain"]:checked')?.value;
        const rainMm = parseFloat(document.getElementById('f3_rainfall_mm')?.value);
        if (rainPrecip === '1' || rainHeavy === '1' || (!isNaN(rainMm) && rainMm >= 10.0)) {
            exposedFactors.push({
                name: 'พายุฝนตกหนักวิกฤต (Torrential Rain ≥ 10.0 มม./ชม.)',
                desc: 'ทัศนวิสัยบกพร่อง ถนนลื่น และการเดินเรือชะลอตัวจากฝนตกหนักสะสม',
                icon: '🌧️'
            });
        }

        // Determinant 6: Pier queue congestion
        const pierCongest = document.querySelector('input[name="f2_pier_congestion"]:checked')?.value;
        if (pierCongest === '1') {
            exposedFactors.push({
                name: 'คิวรถติดสะสมหน้าท่าเรือข้ามฟาก (Pier Queue Congestion)',
                desc: 'มีรถติดสะสมหน้าท่าเรือคลองหมาก ไม่สามารถนำรถพยาบาลขึ้นแพได้ทันที',
                icon: '🚗'
            });
        }

        // Determinant 7: Public long holiday >= 3 days
        const holiday = document.querySelector('input[name="f3_holiday"]:checked')?.value;
        if (holiday === '1') {
            exposedFactors.push({
                name: 'วันหยุดยาวราชการ / เทศกาลท่องเที่ยว (Public Long Holiday ≥ 3 วัน)',
                desc: 'ปริมาณยานพาหนะและนักท่องเที่ยวหนาแน่น ก่อให้เกิดความล่าช้าในการสัญจร',
                icon: '🏖️'
            });
        }

        // Determinant 8: Night ED Shift (00:00-08:00)
        const f1Shift = document.querySelector('input[name="f1_shift"]:checked')?.value;
        const f3Shift = document.querySelector('input[name="f3_ed_shift"]:checked')?.value;
        if (f1Shift === 'night' || f3Shift === 'night') {
            exposedFactors.push({
                name: 'เวรดึกห้องฉุกเฉินเกาะลันตา (Night ED Shift: 00:00–08:00 น.)',
                desc: 'การระดมทรัพยากร บุคลากร และทีมประสานส่งต่อนอกเวลาปฏิบัติการหลัก',
                icon: '🌙'
            });
        }

        // Determinant 9: System Total Referral Delay (T_Total > Benchmark)
        const isTrauma = Boolean(document.getElementById('f1_inc4_trauma')?.checked);
        const totalMin = parseInt(document.getElementById('f2_t_total_min')?.value, 10);
        const totalLimit = isTrauma ? 156 : 141;
        const isTotalDelay = document.getElementById('f2_total_delay')?.checked || (!isNaN(totalMin) && totalMin > totalLimit);
        if (isTotalDelay) {
            exposedFactors.push({
                name: 'ระบบส่งต่อรวมล่าช้าเกินเกณฑ์มาตรฐาน (Total System Delay: T_Total > เกณฑ์)',
                desc: `เวลารวมทั้งระบบ ${!isNaN(totalMin) ? totalMin + ' นาที ' : ''}เกินเกณฑ์มาตรฐาน (เกณฑ์: ${totalLimit} นาที)`,
                icon: '⏱️'
            });
        }

        const hasLogisticsData = (ferryF2 !== undefined || ferryF3 !== undefined || season !== undefined ||
                                  tideLow !== undefined || seaState !== undefined || rainPrecip !== undefined ||
                                  pierCongest !== undefined || holiday !== undefined || f1Shift !== undefined ||
                                  f3Shift !== undefined || isOffHour || !isNaN(totalMin));

        const isExposed = exposedFactors.length > 0;

        if (isExposed) {
            cohortBadge.innerHTML = `
                <div style="display: inline-flex; align-items: center; gap: 8px; background: #fef2f2; border: 1.5px solid #ef4444; color: #991b1b; padding: 6px 12px; border-radius: 6px; font-weight: 800; font-size: 13.5px; box-shadow: 0 1px 3px rgba(239,68,68,0.12);">
                    <span style="font-size: 16px;">⚠️</span>
                    <span>EXPOSED GROUP (กลุ่มสัมผัสปัจจัยคุกคาม)</span>
                </div>
            `;
            let factorsHtml = '<div style="display: flex; flex-direction: column; gap: 6px; margin-top: 6px;">';
            exposedFactors.forEach(f => {
                factorsHtml += `
                    <div style="background: #ffffff; border: 1px solid #fee2e2; border-left: 3.5px solid #ef4444; border-radius: 5px; padding: 6px 10px;">
                        <div style="font-weight: 700; color: #991b1b; font-size: 12.5px;">${f.icon} ${f.name}</div>
                        <div style="color: #64748b; font-size: 11px; margin-top: 1px;">${f.desc}</div>
                    </div>
                `;
            });
            factorsHtml += `
                <div style="font-size: 11.5px; color: #b91c1c; font-weight: 700; margin-top: 4px; display: flex; align-items: center; gap: 4px;">
                    <span>📌 ตรวจพบปัจจัยคุกคามสะสมรวม:</span> <span style="background: #fee2e2; padding: 1px 6px; border-radius: 10px;">${exposedFactors.length} ปัจจัย</span>
                </div>
            </div>`;
            cohortFactorsEl.innerHTML = factorsHtml;
        } else if (hasLogisticsData) {
            cohortBadge.innerHTML = `
                <div style="display: inline-flex; align-items: center; gap: 8px; background: #f0fdf4; border: 1.5px solid #22c55e; color: #166534; padding: 6px 12px; border-radius: 6px; font-weight: 800; font-size: 13.5px; box-shadow: 0 1px 3px rgba(34,197,94,0.12);">
                    <span style="font-size: 16px;">✅</span>
                    <span>CONTROL GROUP (กลุ่มควบคุม / ปลอดปัจจัยคุกคาม)</span>
                </div>
            `;
            cohortFactorsEl.innerHTML = `
                <div style="background: #ffffff; border: 1px solid #bbf7d0; border-left: 3.5px solid #22c55e; border-radius: 5px; padding: 8px 10px; margin-top: 6px; color: #166534; font-size: 12px; line-height: 1.5;">
                    <div style="font-weight: 700; margin-bottom: 2px;">✓ ไม่พบปัจจัยคุกคามจากการขนส่งและสิ่งแวดล้อม</div>
                    <div style="color: #475569; font-size: 11.5px;">เคสนี้ส่งต่อในสภาวะปกติ (ช่วงกลางวัน 05:00–24:00 น., ทะเลสงบ, น้ำทะเลปกติ, ไม่มีพายุฝน, ท่าเรือไม่ติดขัด, เวรปกติ และส่งต่อตรงเวลา)</div>
                </div>
            `;
        } else {
            cohortBadge.innerHTML = `
                <div style="display: inline-flex; align-items: center; gap: 6px; background: #f8fafc; border: 1px solid #cbd5e1; color: #64748b; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 12.5px;">
                    <span>ℹ️ รอข้อมูลปัจจัยแวดล้อม (Form 2 & Form 3)</span>
                </div>
            `;
            cohortFactorsEl.innerHTML = `
                <div style="color: #94a3b8; font-size: 12px; font-style: italic; margin-top: 6px;">
                    ยังไม่มีข้อมูลปัจจัยด้านสิ่งแวดล้อมหรือกะเวลาเดินแพ ระบบจะประเมินผลอัตโนมัติเมื่อกรอก Form 2 และ Form 3
                </div>
            `;
        }

        // --- 2. MICRO-TIMELINE DELAYS ASSESSMENT ---
        const isStemi = Boolean(document.getElementById('f1_inc4_stemi')?.checked);
        const isStroke = Boolean(document.getElementById('f1_inc4_ais')?.checked);

        const timelineList = [];

        // 1. T0-1 Island DIDO
        const didoMin = parseInt(document.getElementById('f2_t0_1_min')?.value || document.getElementById('f1_dido_min')?.value, 10);
        const didoLimit = isTrauma ? 60 : 45;
        const hasDido = !isNaN(didoMin) && didoMin >= 0;
        const didoDelayed = hasDido ? (didoMin > didoLimit) : Boolean(document.getElementById('f2_dido_delay')?.checked || document.getElementById('f1_dido_delay')?.checked);
        timelineList.push({
            id: 'T0-1',
            name: 'T0-1 Island DIDO (รพ.เกาะลันตา)',
            desc: 'ประเมิน คืนชีพ วินิจฉัย และเตรียมส่งต่อในห้องฉุกเฉิน',
            benchmark: didoLimit,
            benchmarkStr: `≤ ${didoLimit} นาที (${isTrauma ? 'Trauma' : 'Stroke/STEMI'})`,
            actual: hasDido ? didoMin : null,
            delayed: didoDelayed,
            hasData: hasDido || document.getElementById('f2_dido_ontime')?.checked || document.getElementById('f2_dido_delay')?.checked
        });

        // 2. T2 Island Road
        const t2Min = parseInt(document.getElementById('f2_t2_min')?.value, 10);
        const hasT2 = !isNaN(t2Min) && t2Min >= 0;
        const t2Delayed = hasT2 ? (t2Min > 12) : Boolean(document.getElementById('f2_road_delay')?.checked);
        timelineList.push({
            id: 'T2',
            name: 'T2 Island Road (ถนนบนเกาะ)',
            desc: 'วิ่งจาก รพ.เกาะลันตา ไปยังท่าเรือคลองหมาก (7.0 กม.)',
            benchmark: 12,
            benchmarkStr: '≤ 12 นาที',
            actual: hasT2 ? t2Min : null,
            delayed: t2Delayed,
            hasData: hasT2 || document.getElementById('f2_road_ontime')?.checked || document.getElementById('f2_road_delay')?.checked
        });

        // 3. T_wait Pier Queue Waiting
        const waitMin = parseInt(document.getElementById('f2_t_wait_min')?.value, 10);
        const hasWait = !isNaN(waitMin) && waitMin >= 0;
        const waitDelayed = hasWait ? (waitMin > 5) : Boolean(document.getElementById('f2_wait_delay')?.checked);
        timelineList.push({
            id: 'T_wait',
            name: 'T_wait Pier Waiting (รอขึ้นแพ)',
            desc: 'เวลารอคิว / รอเรียกแพขนานยนต์ ณ ท่าเรือคลองหมาก',
            benchmark: 5,
            benchmarkStr: '≤ 5 นาที',
            actual: hasWait ? waitMin : null,
            delayed: waitDelayed,
            hasData: hasWait || document.getElementById('f2_wait_ontime')?.checked || document.getElementById('f2_wait_delay')?.checked
        });

        // 4. T3 Ferry Crossing
        const t3Min = parseInt(document.getElementById('f2_t3_min')?.value, 10);
        const hasT3 = !isNaN(t3Min) && t3Min >= 0;
        const t3Delayed = hasT3 ? (t3Min > 24) : Boolean(document.getElementById('f2_water_delay')?.checked);
        timelineList.push({
            id: 'T3',
            name: 'T3 Ferry Crossing (ข้ามร่องน้ำ)',
            desc: 'แพขนานยนต์ข้ามร่องน้ำเกาะลันตา (1.53 กม.)',
            benchmark: 24,
            benchmarkStr: '≤ 24 นาที',
            actual: hasT3 ? t3Min : null,
            delayed: t3Delayed,
            hasData: hasT3 || document.getElementById('f2_water_ontime')?.checked || document.getElementById('f2_water_delay')?.checked
        });

        // 5. T4 Mainland Highway
        const t4Min = parseInt(document.getElementById('f2_t4_min')?.value, 10);
        const hasT4 = !isNaN(t4Min) && t4Min >= 0;
        const t4Delayed = hasT4 ? (t4Min > 60) : Boolean(document.getElementById('f2_hwy_delay')?.checked);
        timelineList.push({
            id: 'T4',
            name: 'T4 Mainland Highway (ทางหลวง)',
            desc: 'วิ่งจากท่าบ้านหัวหิน ถึง ER รพ.กระบี่ (71.0 กม.)',
            benchmark: 60,
            benchmarkStr: '≤ 60 นาที',
            actual: hasT4 ? t4Min : null,
            delayed: t4Delayed,
            hasData: hasT4 || document.getElementById('f2_hwy_ontime')?.checked || document.getElementById('f2_hwy_delay')?.checked
        });

        // 6. T_Total System Transfer Time
        const hasTotal = !isNaN(totalMin) && totalMin >= 0;
        const totalDelayed = hasTotal ? (totalMin > totalLimit) : Boolean(document.getElementById('f2_total_delay')?.checked);
        timelineList.push({
            id: 'T_Total',
            name: 'T_Total Referral System (เวลารวมระบบ)',
            desc: 'รวมเวลาตั้งแต่ ER ลันตา ถึง ER รพ.กระบี่ (T0-1+T2+T3+T4)',
            benchmark: totalLimit,
            benchmarkStr: `≤ ${totalLimit} นาที (${isTrauma ? 'Trauma' : 'Stroke/STEMI'})`,
            actual: hasTotal ? totalMin : null,
            delayed: totalDelayed,
            hasData: hasTotal || document.getElementById('f2_total_ontime')?.checked || document.getElementById('f2_total_delay')?.checked
        });

        // 7. T4-5 Door-to-Intervention (Mainland ED)
        const t45Min = parseInt(document.getElementById('f4_t4_5_min')?.value, 10);
        const hasT45 = !isNaN(t45Min) && t45Min >= 0;
        const t45Delayed = hasT45 ? (t45Min > 30) : false;
        timelineList.push({
            id: 'T4-5',
            name: 'T4-5 Door-to-Intervention (รพ.กระบี่)',
            desc: 'เวลาตั้งแต่ถึง ER รพ.กระบี่ จนถึงส่งต่อหัตถการกู้ชีพ/หอผู้ป่วย',
            benchmark: 30,
            benchmarkStr: '≤ 30 นาที',
            actual: hasT45 ? t45Min : null,
            delayed: t45Delayed,
            hasData: hasT45
        });

        // 8. Disease-specific Golden Window
        if (isStemi) {
            const d2b = parseInt(document.getElementById('f4_pci_d2b_min')?.value, 10);
            const hasD2b = !isNaN(d2b) && d2b >= 0;
            const d2bDelayed = hasD2b ? (d2b > 180) : Boolean(document.getElementById('f4_pci_missed')?.checked);
            timelineList.push({
                id: 'Golden-STEMI',
                name: 'STEMI Door-to-Balloon (PCI Golden Window)',
                desc: 'เวลาเข้า ER ลันตา ถึงบอลลูนเปิดหลอดเลือดหัวใจ (ESC Remote Island)',
                benchmark: 180,
                benchmarkStr: '≤ 180 นาที',
                actual: hasD2b ? d2b : null,
                delayed: d2bDelayed,
                hasData: hasD2b || document.getElementById('f4_pci_achieved')?.checked || document.getElementById('f4_pci_missed')?.checked
            });
        } else if (isStroke) {
            const o2n = parseInt(document.getElementById('f4_stroke_o2n_min')?.value, 10);
            const hasO2n = !isNaN(o2n) && o2n >= 0;
            const o2nDelayed = hasO2n ? (o2n > 270) : Boolean(document.getElementById('f4_stroke_missed')?.checked);
            timelineList.push({
                id: 'Golden-Stroke',
                name: 'Stroke Onset-to-Needle (rtPA Golden Window)',
                desc: 'เวลาเริ่มมีอาการ ถึงเริ่มฉีดยาละลายลิ่มเลือด (IV rtPA ≤ 4.5 ชม.)',
                benchmark: 270,
                benchmarkStr: '≤ 270 นาที (4.5 ชม.)',
                actual: hasO2n ? o2n : null,
                delayed: o2nDelayed,
                hasData: hasO2n || document.getElementById('f4_stroke_achieved')?.checked || document.getElementById('f4_stroke_missed')?.checked
            });
        } else if (isTrauma) {
            const traumaMissed = Boolean(document.getElementById('f4_trauma_missed')?.checked);
            const traumaAchieved = Boolean(document.getElementById('f4_trauma_achieved')?.checked);
            const ctMin = parseInt(document.getElementById('f4_trauma_d2ct_min')?.value, 10);
            const orMin = parseInt(document.getElementById('f4_trauma_d2or_min')?.value, 10);
            const hasTrauma = traumaMissed || traumaAchieved || (!isNaN(ctMin) && ctMin >= 0) || (!isNaN(orMin) && orMin >= 0);
            let traumaActualStr = '';
            if (!isNaN(ctMin) && ctMin >= 0) traumaActualStr += `CT: ${ctMin}m `;
            if (!isNaN(orMin) && orMin >= 0) traumaActualStr += `OR: ${orMin}m`;
            timelineList.push({
                id: 'Golden-Trauma',
                name: 'Trauma Resuscitation Window (CT / OR)',
                desc: 'เกณฑ์เวลาทำ CT (≤ 150 นาที) หรือเข้าห้องผ่าตัดฉุกเฉิน (OR ≤ 180 นาที)',
                benchmarkStr: 'CT ≤ 150m / OR ≤ 180m',
                actual: traumaActualStr.trim() || null,
                delayed: traumaMissed,
                hasData: hasTrauma
            });
        }

        const evaluatedTimelines = timelineList.filter(t => t.hasData);
        const delayedTimelines = evaluatedTimelines.filter(t => t.delayed);

        // Update delay count badge
        if (delayBadge) {
            if (evaluatedTimelines.length === 0) {
                delayBadge.style.background = '#f1f5f9';
                delayBadge.style.color = '#64748b';
                delayBadge.innerText = 'รอข้อมูลเวลา';
            } else if (delayedTimelines.length > 0) {
                delayBadge.style.background = '#fee2e2';
                delayBadge.style.color = '#991b1b';
                delayBadge.innerText = `⚠️ ล่าช้า ${delayedTimelines.length} / ${evaluatedTimelines.length} ช่วง`;
            } else {
                delayBadge.style.background = '#dcfce7';
                delayBadge.style.color = '#166534';
                delayBadge.innerText = `✓ ตรงเวลาทุกช่วง (${evaluatedTimelines.length}/${evaluatedTimelines.length})`;
            }
        }

        // Update summary badge
        if (timelineSummary) {
            if (evaluatedTimelines.length === 0) {
                timelineSummary.innerHTML = `
                    <div style="display: inline-flex; align-items: center; gap: 6px; background: #f8fafc; border: 1px solid #cbd5e1; color: #64748b; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 12.5px;">
                        <span>ℹ️ ยังไม่มีการบันทึกข้อมูลเวลาส่งต่อ (Form 2 & Form 4)</span>
                    </div>
                `;
            } else if (delayedTimelines.length > 0) {
                timelineSummary.innerHTML = `
                    <div style="display: inline-flex; align-items: center; gap: 8px; background: #fef2f2; border: 1.5px solid #ef4444; color: #991b1b; padding: 6px 12px; border-radius: 6px; font-weight: 800; font-size: 13.5px; box-shadow: 0 1px 3px rgba(239,68,68,0.12);">
                        <span style="font-size: 16px;">⏱️</span>
                        <span>พบจุดคอขวดเวลาล่าช้า (Delayed Referral Process)</span>
                    </div>
                `;
            } else {
                timelineSummary.innerHTML = `
                    <div style="display: inline-flex; align-items: center; gap: 8px; background: #f0fdf4; border: 1.5px solid #22c55e; color: #166534; padding: 6px 12px; border-radius: 6px; font-weight: 800; font-size: 13.5px; box-shadow: 0 1px 3px rgba(34,197,94,0.12);">
                        <span style="font-size: 16px;">⚡</span>
                        <span>ระบบส่งต่อตรงเวลาตามเกณฑ์มาตรฐานทุกช่วง (Optimal Timelines)</span>
                    </div>
                `;
            }
        }

        // Render intervals breakdown list
        let delaysHtml = '<div style="display: flex; flex-direction: column; gap: 6px; margin-top: 6px;">';
        timelineList.forEach(t => {
            const hasData = t.hasData;
            const isDelayed = t.delayed;
            let statusBadge = '';

            if (!hasData) {
                statusBadge = '<span style="color: #94a3b8; font-size: 11px; font-style: italic; background: #f8fafc; padding: 2px 6px; border-radius: 4px; border: 1px dashed #cbd5e1;">รอข้อมูลเวลา</span>';
            } else if (isDelayed) {
                let diffText = '';
                if (typeof t.actual === 'number' && typeof t.benchmark === 'number') {
                    const diff = t.actual - t.benchmark;
                    diffText = ` (+${diff} นาที)`;
                }
                statusBadge = `<span style="background: #fee2e2; color: #991b1b; border: 1px solid #f87171; padding: 2px 7px; border-radius: 4px; font-weight: 800; font-size: 11.5px;">⚠️ ล่าช้า${diffText}</span>`;
            } else {
                let diffText = '';
                if (typeof t.actual === 'number' && typeof t.benchmark === 'number') {
                    const diff = t.benchmark - t.actual;
                    diffText = diff > 0 ? ` (เร็วว่า ${diff} นาที)` : ' (ทันเกณฑ์)';
                }
                statusBadge = `<span style="background: #dcfce7; color: #166534; border: 1px solid #86efac; padding: 2px 7px; border-radius: 4px; font-weight: 800; font-size: 11.5px;">✓ ตรงเวลา${diffText}</span>`;
            }

            const borderColor = !hasData ? '#e2e8f0' : (isDelayed ? '#fca5a5' : '#bbf7d0');
            const borderLeftColor = !hasData ? '#94a3b8' : (isDelayed ? '#ef4444' : '#22c55e');
            const bgColor = !hasData ? '#ffffff' : (isDelayed ? '#fffbfb' : '#fafffc');

            delaysHtml += `
                <div style="background: ${bgColor}; border: 1px solid ${borderColor}; border-left: 3.5px solid ${borderLeftColor}; border-radius: 5px; padding: 6px 10px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
                    <div style="flex: 1; min-width: 180px;">
                        <div style="font-weight: 700; font-size: 12.5px; color: ${isDelayed ? '#991b1b' : '#1e293b'};">
                            ${t.name}
                        </div>
                        <div style="font-size: 11px; color: #64748b; margin-top: 1px;">
                            ${t.desc} • <span style="color: #475569; font-weight: 600;">เกณฑ์: ${t.benchmarkStr}</span>
                            ${hasData && t.actual !== null ? ` • <b style="color: ${isDelayed ? '#dc2626' : '#15803d'};">เวลาจริง: ${t.actual} นาที</b>` : ''}
                        </div>
                    </div>
                    <div>
                        ${statusBadge}
                    </div>
                </div>
            `;
        });

        // Add summary note of delayed intervals if any
        if (delayedTimelines.length > 0) {
            delaysHtml += `
                <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 5px; padding: 6px 10px; margin-top: 4px; font-size: 11.5px; color: #991b1b;">
                    <b>🚨 สรุปช่วงเวลาที่นับเป็นล่าช้า (${delayedTimelines.length} ช่วง):</b>
                    <ul style="margin: 3px 0 0 16px; padding: 0;">
                        ${delayedTimelines.map(t => `<li><b>${t.name}</b>: ${t.actual !== null ? `ใช้เวลา ${t.actual} นาที (เกณฑ์ ${t.benchmarkStr})` : 'เกินเกณฑ์มาตรฐาน'}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        delaysHtml += '</div>';
        timelineDelaysEl.innerHTML = delaysHtml;
    }

    function calcAll() {
        pullT0T1FromForm1();
        calcScreening();
        calcCCI();
        calcVitals();
        calcGCS();
        calcRTS();
        calcTimelines();
        calcForm2Timelines();
        calcCompositeAE();
        calcForm3();
        calcKrabiVitals();
        calcKrabiGCS();
        calcDeltaKillip();
        calcDeltaGCS();
        calcDeltaRTS();
        calcDeltaVitals();
        calcDeltaBT();
        calcForm4Timelines();
        toggleCprDetails();
        toggleMortalityDetails();
        autoDetectFerryOperate();
        if (typeof updateEpidemiologicalAssessment === 'function') updateEpidemiologicalAssessment();
    }

    // --- CASE MANAGEMENT & LOCAL STORAGE ---
    let autoSaveTimeout = null;

    function scheduleAutoSave() {
        clearTimeout(autoSaveTimeout);
        autoSaveTimeout = setTimeout(() => {
            saveCurrentCase(true);
        }, 800);
    }

    function initAutoSave() {
        document.querySelectorAll('input, select').forEach(el => {
            el.addEventListener('change', () => {
                if (typeof updateEpidemiologicalAssessment === 'function') updateEpidemiologicalAssessment();
                scheduleAutoSave();
            });
            el.addEventListener('input', () => {
                if (typeof updateEpidemiologicalAssessment === 'function') updateEpidemiologicalAssessment();
                scheduleAutoSave();
            });
        });
    }

    function getFormData() {
        const data = {};
        document.querySelectorAll('input, select, textarea').forEach(el => {
            if (el.type === 'radio') {
                if (el.checked) {
                    data[el.name] = el.value;
                    if (el.id) data[el.id] = true;
                }
            } else if (el.type === 'checkbox') {
                data[el.id || el.name] = el.checked;
            } else {
                data[el.id || el.name] = el.value;
            }
        });

        // Epidemiological Evaluation Summary
        const cohortStatusBadge = document.getElementById('cohort_badge_container')?.innerText || '';
        const isExposed = cohortStatusBadge.includes('EXPOSED');
        const isControl = cohortStatusBadge.includes('CONTROL');
        data['cohort_classification'] = isExposed ? 'Exposed' : (isControl ? 'Control' : 'Pending');

        // Extract list of active exposure determinants
        const factorEls = document.querySelectorAll('#cohort_factors_container [style*="font-weight: 700"]');
        const factors = [];
        factorEls.forEach(el => {
            const txt = el.innerText.trim();
            if (txt && !txt.startsWith('✓') && !txt.startsWith('📌')) factors.push(txt);
        });
        data['cohort_factors'] = factors.join('; ');

        // Extract delayed intervals
        const delayedSummaryLi = document.querySelectorAll('#timeline_delays_container ul li');
        const delayedList = [];
        delayedSummaryLi.forEach(li => delayedList.push(li.innerText.trim()));
        data['timeline_delayed_intervals'] = delayedList.join('; ');
        data['timeline_delay_count'] = delayedList.length;
        data['timeline_overall_status'] = delayedList.length > 0 ? 'Delayed' : (document.getElementById('delay_count_badge')?.innerText.includes('ตรงเวลา') ? 'On-time' : 'Pending');

        return data;
    }

    function setFormData(data) {
        if (!data) return;
        document.querySelectorAll('input, select, textarea').forEach(el => {
            const key = el.id || el.name;
            if (el.type === 'radio') {
                if (data[el.name] !== undefined && el.value === data[el.name]) {
                    el.checked = true;
                } else if (el.id && data[el.id] === true) {
                    el.checked = true;
                } else {
                    el.checked = false;
                }
            } else if (el.type === 'checkbox') {
                if (data[key] !== undefined) {
                    el.checked = Boolean(data[key]);
                } else if (key === 'f2_amb_type') {
                    el.checked = true;
                } else {
                    el.checked = false;
                }
            } else {
                if (data[key] !== undefined) {
                    el.value = data[key];
                }
            }
        });

        // Sync active disease visuals & isolation
        const disease = getActiveDisease();
        applyDiseaseIsolation(disease);
        updateDiseaseVisuals(disease);

        toggleCprDetails();
        toggleMortalityDetails();
        toggleRainDetails();
        autoDetectFerryOperate();

        calcAll();
    }

    function saveCurrentCase(isAuto = false) {
        const studyId = document.getElementById('f1_study_id')?.value.trim() || 'UNNAMED';
        const key = 'online_crf_case_' + studyId;
        const formData = getFormData();
        formData.lastUpdated = new Date().toISOString();
        formData.studyId = studyId;

        localStorage.setItem(key, JSON.stringify(formData));
        localStorage.setItem('online_crf_last_active_id', studyId);

        // Update Case Index
        let index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
        if (!index.includes(studyId)) {
            index.push(studyId);
            localStorage.setItem('online_crf_case_index', JSON.stringify(index));
            loadCaseIndex();
        }

        const statusEl = document.getElementById('save-status');
        if (statusEl) {
            const timeStr = new Date().toLocaleTimeString();
            statusEl.innerHTML = '✓ ' + (isAuto ? 'บันทึกอัตโนมัติ' : 'บันทึกเรียบร้อย') + ' (' + timeStr + ')';
            statusEl.style.display = 'inline-flex';
        }

        if (!isAuto) {
            const disease = getActiveDisease();
            if (!disease) {
                alert('⚠️ บันทึกข้อมูลฉบับร่างแล้ว แต่ยังไม่ได้ติ๊กเลือกกลุ่มโรคในเกณฑ์การคัดเข้าข้อ 4\\n(บังคับเลือก 1 กลุ่มโรค: STEMI, Acute Ischemic Stroke หรือ Severe Trauma)');
                const alertEl = document.getElementById('f1_inc4_disease_alert');
                if (alertEl) {
                    alertEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    alertEl.style.boxShadow = '0 0 14px rgba(244, 63, 94, 0.9)';
                    setTimeout(() => { alertEl.style.boxShadow = ''; }, 2500);
                }
            }
        }
    }

    function loadCaseIndex() {
        const select = document.getElementById('case-selector');
        if (!select) return;
        const index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
        select.innerHTML = '<option value="">-- เลือกเคสที่บันทึกไว้ --</option>';
        index.forEach(id => {
            const opt = document.createElement('option');
            opt.value = id;
            opt.textContent = 'LANTA_' + id;
            select.appendChild(opt);
        });
        const curId = document.getElementById('f1_study_id')?.value.trim();
        if (curId && index.includes(curId)) select.value = curId;
    }

    function onCaseSelected(sel) {
        const id = sel.value;
        if (id) loadCase(id);
    }

    function loadCase(studyId) {
        const raw = localStorage.getItem('online_crf_case_' + studyId);
        if (!raw) return;
        const data = JSON.parse(raw);
        setFormData(data);
        localStorage.setItem('online_crf_last_active_id', studyId);
        loadCaseIndex();
    }

    function createNewCase() {
        if (confirm('ต้องการสร้างเคสใหม่ใช่หรือไม่? (ข้อมูลปัจจุบันได้รับการบันทึกแล้ว)')) {
            const index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
            let nextNum = (index.length + 1).toString().padStart(3, '0');
            
            // Clear inputs
            document.querySelectorAll('input:not([type="radio"]):not([type="checkbox"])').forEach(el => el.value = '');
            document.querySelectorAll('input[type="radio"], input[type="checkbox"]').forEach(el => el.checked = false);

            document.getElementById('f1_study_id').value = nextNum;
            syncFields('study-id-sync', nextNum);
            
            // ALS Ambulance always checked!
            const ambEl = document.getElementById('f2_amb_type');
            if (ambEl) ambEl.checked = true;

            applyDiseaseIsolation(null);
            updateDiseaseVisuals(null);

            toggleCprDetails();
            toggleMortalityDetails();
            toggleRainDetails();

            calcAll();
            saveCurrentCase(true);
            switchTab(1);
        }
    }

    // --- EXCEL EXPORT (SHEETJS) ---
    function exportToExcel() {
        if (typeof XLSX === 'undefined') {
            alert('ไม่พบไลบรารี SheetJS กรุณาตรวจสอบไฟล์ xlsx.full.min.js ในโฟลเดอร์');
            return;
        }

        saveCurrentCase(false);

        const index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
        if (index.length === 0) {
            alert('ไม่มีข้อมูลเคสสำหรับ Export');
            return;
        }

        const wb = XLSX.utils.book_new();

        const masterRows = [];
        const form1Rows = [];
        const form2Rows = [];
        const form3Rows = [];
        const form4Rows = [];

        index.forEach(id => {
            const raw = localStorage.getItem('online_crf_case_' + id);
            if (!raw) return;
            const c = JSON.parse(raw);

            // Master Flattened Row (Best for Stata/SPSS/R)
            masterRows.push({
                STUDY_ID: 'LANTA_' + (c.f1_study_id || id),
                Refer_ID: c.f1_refer_id || '',
                HN: c.f1_hn || '',
                VN: c.f1_vn || '',
                Abstract_Date: c.f1_abs_date || '',
                Abstractor: c.f1_abstractor || '',
                Eligible_Status: c.f1_eligible || '',
                Age: c.f1_age || '',
                Sex: c.f1_sex || '',
                Residency: c.f1_residency || '',
                Nationality: c.f1_nationality || '',
                Premorbid_mRS: c.f1_premrs || '',
                CCI_Total: c.f1_cci_total || '',
                Onset_Date: c.f1_onset_date || '',
                Onset_Time: c.f1_onset_time || '',
                Onset_to_ER_min: c.f1_onset_to_er || '',
                T0_Date: c.f1_t0_date || '',
                T0_Time: c.f1_t0_time || '',
                Arrival_Mode: c.f1_arrival_mode || '',
                Triage_ESI: c.f1_esi || '',
                ED_Shift: c.f1_shift || '',
                Target_Disease: c.f1_target_disease || (c.f1_inc4_stemi ? 'STEMI' : (c.f1_inc4_ais ? 'AIS' : (c.f1_inc4_trauma ? 'Trauma' : ''))),
                Disease_STEMI: (c.f1_target_disease === 'stemi' || c.f1_inc4_stemi) ? 1 : 0,
                Disease_AIS: (c.f1_target_disease === 'ais' || c.f1_inc4_ais) ? 1 : 0,
                Disease_Trauma: (c.f1_target_disease === 'trauma' || c.f1_inc4_trauma) ? 1 : 0,
                Lanta_Killip: c.f1_killip || '',
                Lanta_Stroke_GCS: c.f1_stroke_gcs || '',
                Lanta_Trauma_Acuity: c.f1_trauma_acuity || '',
                Lanta_SBP: c.f1_sbp || '',
                Lanta_DBP: c.f1_dbp || '',
                Lanta_MAP: c.f1_map || '',
                Lanta_HR: c.f1_hr || '',
                Lanta_RR: c.f1_rr || '',
                Lanta_SpO2: c.f1_spo2 || '',
                Lanta_BT: c.f1_bt || '',
                Lanta_MSI: c.f1_msi || '',
                Lanta_Total_GCS: c.f1_gcs_total || '',
                Lanta_Total_RTS: c.f1_rts_total || '',
                PreIntubation: c.f1_intubation || '',
                PreInotropes: c.f1_inotropes || '',
                T1_Date: c.f1_t1_date || '',
                T1_Time: c.f1_t1_time || '',
                T0_1_DIDO_min: c.f1_dido_min || '',
                DIDO_Eval: c.f1_dido_eval || '',
                // Form 2
                Ambulance_Plate: c.f2_amb_plate || '',
                Escort_RN: c.f2_escort_rn || '',
                Driver: c.f2_driver || '',
                T2_Port_Date: c.f2_t2_date || '',
                T2_Port_Time: c.f2_t2_time || '',
                T3_Embark_Date: c.f2_t3_embark_date || '',
                T3_Embark_Time: c.f2_t3_embark_time || '',
                T3_Disembark_Date: c.f2_t3_disembark_date || '',
                T3_Disembark_Time: c.f2_t3_disembark_time || '',
                T4_Krabi_Date: c.f2_t4_date || '',
                T4_Krabi_Time: c.f2_t4_time || '',
                T5_Definitive_Date: c.f2_t5_date || '',
                T5_Definitive_Time: c.f2_t5_time || '',
                T2_IslandRoad_min: c.f2_t2_min || '',
                T3_WaterCrossing_min: c.f2_t3_min || '',
                T_WaitPier_min: c.f2_t_wait_min || '',
                T4_MainlandHwy_min: c.f2_t4_min || '',
                T_Total_min: c.f2_t_total_min || '',
                T5_Definitive_min: c.f2_t5_min || '',
                Ferry_Operate: c.f2_ferry_operate || '',
                Pier_Congestion: c.f2_pier_congestion || '',
                Ferry_Count: c.f2_ferry_count || '',
                Composite_InTransit_AE: c.f2_composite_ae || '',
                // Form 3
                T3_Marine_Date: c.f3_t3_date || '',
                T3_Marine_Time: c.f3_t3_time || '',
                Tide_Height_m: c.f3_tide_height || '',
                Tide_Extreme_Low: c.f3_tide_extreme || '',
                Tide_Phase: c.f3_tide_phase || '',
                Sandbar_Grounding_Risk: c.f3_sandbar_risk || '',
                Season_Monsoon: c.f3_season || '',
                Sea_State: c.f3_sea_state || '',
                Wind_Speed_Knots: c.f3_wind_speed || '',
                Wind_Direction: c.f3_wind_direction || '',
                Precipitation: c.f3_precipitation || '',
                Torrential_Rain_Rate: c.f3_torrential_rain || '',
                Rainfall_Hourly_mm: c.f3_rainfall_mm || '',
                Holiday_Status: c.f3_holiday || '',
                Ferry_Shift_Hours: c.f3_ferry_shift || '',
                // Form 4
                Krabi_HN: c.f4_krabi_hn || '',
                Krabi_Ward: c.f4_ward || '',
                Krabi_SBP: c.f4_sbp || '',
                Krabi_DBP: c.f4_dbp || '',
                Krabi_MAP: c.f4_map || '',
                Krabi_HR: c.f4_hr || '',
                Krabi_RR: c.f4_rr || '',
                Krabi_SpO2: c.f4_spo2 || '',
                Krabi_BT: c.f4_bt || '',
                Krabi_GCS_Total: c.f4_gcs_total || '',
                Krabi_MSI: c.f4_msi || '',
                Krabi_Killip: c.f4_killip || '',
                Delta_Killip_Eval: c.f4_eval_killip || '',
                Delta_GCS_Score: c.f4_delta_gcs || '',
                Delta_GCS_Eval: c.f4_eval_gcs || '',
                Delta_RTS_Score: c.f4_delta_rts || '',
                Delta_RTS_Eval: c.f4_eval_rts || '',
                Delta_MSI_Score: c.f4_delta_msi || '',
                Delta_MSI_Eval: c.f4_eval_msi || '',
                Delta_MAP_mmHg: c.f4_delta_map || '',
                Delta_MAP_Eval: c.f4_eval_map || '',
                Delta_BT_C: c.f4_delta_bt || '',
                Delta_BT_Eval: c.f4_eval_bt || '',
                Composite_Deterioration: c.f4_composite_deter || '',
                Door_to_Intervention_min: c.f4_t4_5_min || '',
                STEMI_D2B_min: c.f4_pci_d2b_min || '',
                STEMI_GoldenWindow: c.f4_eval_pci || '',
                Stroke_O2N_min: c.f4_stroke_o2n_min || '',
                Stroke_GoldenWindow: c.f4_eval_stroke || '',
                Trauma_D2CT_min: c.f4_trauma_d2ct_min || '',
                Trauma_D2OR_min: c.f4_trauma_d2or_min || '',
                Trauma_GoldenWindow: c.f4_eval_trauma || '',
                Mortality_ER: c.f4_mort_er || '',
                Mortality_24h: c.f4_mort_24h || '',
                Primary_Death_Cause: c.f4_mort_cause || '',
                Cohort_Classification: c.cohort_classification || '',
                Cohort_Exposures: c.cohort_factors || '',
                MicroTimeline_Delay_Count: c.timeline_delay_count !== undefined ? c.timeline_delay_count : '',
                MicroTimeline_Delayed_List: c.timeline_delayed_intervals || '',
                Overall_Referral_Timeliness: c.timeline_overall_status || ''
            });

            // Form 1 specific
            form1Rows.push({
                STUDY_ID: 'LANTA_' + (c.f1_study_id || id),
                Refer_ID: c.f1_refer_id || '',
                HN_Lanta: c.f1_hn || '',
                VN_Lanta: c.f1_vn || '',
                Abstract_Date: c.f1_abs_date || '',
                Abstractor: c.f1_abstractor || '',
                Inclusion_All: c.f1_eligible || '',
                Target_Disease: c.f1_target_disease || (c.f1_inc4_stemi ? 'STEMI' : (c.f1_inc4_ais ? 'AIS' : (c.f1_inc4_trauma ? 'Trauma' : ''))),
                Age: c.f1_age || '',
                Sex: c.f1_sex || '',
                Residency: c.f1_residency || '',
                Nationality: c.f1_nationality || '',
                mRS_Premorbid: c.f1_premrs || '',
                CCI_Total: c.f1_cci_total || '',
                T0_Date: c.f1_t0_date || '',
                T0_Time: c.f1_t0_time || '',
                Onset_Date: c.f1_onset_date || '',
                Onset_Time: c.f1_onset_time || '',
                Onset_to_ER_min: c.f1_onset_to_er || '',
                Arrival_Mode: c.f1_arrival_mode || '',
                Triage_ESI: c.f1_esi || '',
                Island_ED_Shift: c.f1_shift || '',
                Killip_Initial: c.f1_killip || '',
                Stroke_GCS_Conscious: c.f1_stroke_gcs || '',
                Trauma_Mechanism: (c.f1_trauma_mech1 ? 'HighVelocity;' : '') + (c.f1_trauma_mech2 ? 'FallHeight;' : '') + (c.f1_trauma_mech3 ? 'Penetrating;' : ''),
                Trauma_Physiological_Acuity: c.f1_trauma_acuity || '',
                SBP_Lanta: c.f1_sbp || '',
                DBP_Lanta: c.f1_dbp || '',
                MAP_Lanta: c.f1_map || '',
                HR_Lanta: c.f1_hr || '',
                RR_Lanta: c.f1_rr || '',
                SpO2_Lanta: c.f1_spo2 || '',
                BT_Lanta: c.f1_bt || '',
                Hct_Lanta: c.f1_hct || '',
                MSI_Lanta: c.f1_msi || '',
                GCS_Total_Lanta: c.f1_gcs_total || '',
                RTS_Total_Lanta: c.f1_rts_total || '',
                Pre_Intubation: c.f1_intubation || '',
                Pre_Inotropes: c.f1_inotropes || '',
                T1_DoorOut_Date: c.f1_t1_date || '',
                T1_DoorOut_Time: c.f1_t1_time || '',
                T0_1_DIDO_min: c.f1_dido_min || '',
                DIDO_Evaluation: c.f1_dido_eval || ''
            });

            // Form 2 specific
            form2Rows.push({
                STUDY_ID: 'LANTA_' + (c.f2_study_id || id),
                Ambulance_Plate: c.f2_amb_plate || '',
                Escort_RN: c.f2_escort_rn || '',
                Driver: c.f2_driver || '',
                T0_Island_ED_Arrival: ((c.f2_t0_date || c.f1_t0_date || '') + ' ' + (c.f2_t0_time || c.f1_t0_time || '')).trim(),
                T1_Island_ED_DoorOut: ((c.f2_t1_date || c.f1_t1_date || '') + ' ' + (c.f2_t1_time || c.f1_t1_time || '')).trim(),
                T2_Port_Arrival: (c.f2_t2_date || '') + ' ' + (c.f2_t2_time || ''),
                T3_Embark_Ferry: (c.f2_t3_embark_date || '') + ' ' + (c.f2_t3_embark_time || ''),
                T3_Disembark_Port: (c.f2_t3_disembark_date || '') + ' ' + (c.f2_t3_disembark_time || ''),
                T4_Krabi_ED_Door: (c.f2_t4_date || '') + ' ' + (c.f2_t4_time || ''),
                T5_Definitive_Care: (c.f2_t5_date || '') + ' ' + (c.f2_t5_time || ''),
                Interval_T0_1_DIDO_min: c.f2_t0_1_min || '',
                Interval_T2_Road_min: c.f2_t2_min || '',
                Interval_T3_Water_min: c.f2_t3_min || '',
                Interval_WaitPier_min: c.f2_t_wait_min || '',
                Interval_T4_Highway_min: c.f2_t4_min || '',
                Interval_Total_Transit_min: c.f2_t_total_min || '',
                Interval_T5_Definitive_min: c.f2_t5_min || '',
                Ferry_Operation_Shift: c.f2_ferry_operate || '',
                Pier_Congestion_Status: c.f2_pier_congestion || '',
                Active_Ferries_Count: c.f2_ferry_count || '',
                Enroute_Cardiac_Arrest: c.f2_ae_cpr || '',
                Enroute_CPR_Duration_min: c.f2_cpr_duration || '',
                Enroute_Intubation: c.f2_ae_intub || '',
                Enroute_Inotropes_Escalation: c.f2_ae_inotropes || '',
                Enroute_ETT_Dislodgement: c.f2_ae_dislodge || '',
                Enroute_InTransit_Death: c.f2_ae_death || '',
                Composite_InTransit_Deterioration: c.f2_composite_ae || ''
            });

            // Form 3 specific
            form3Rows.push({
                STUDY_ID: 'LANTA_' + (c.f3_study_id || id),
                T3_Date: c.f3_t3_date || '',
                T3_Time: c.f3_t3_time || '',
                Hydro_Station: 'สถานีเกาะลันตาใหญ่ (RTN)',
                Weather_Station: 'สถานีอุตุนิยมวิทยาเกาะลันตา / กระบี่ (TMD)',
                Passage_Coordinates: 'Lat: 7.736 N, Long: 99.062 E',
                Tide_Height_m_LAT: c.f3_tide_height || '',
                Tide_Extreme_Low_Status: c.f3_tide_extreme || '',
                Tide_Phase: c.f3_tide_phase || '',
                Sandbar_Grounding_Risk: c.f3_sandbar_risk || '',
                Season_Monsoon: c.f3_season || '',
                Sea_State: c.f3_sea_state || '',
                Wind_Speed_Knots: c.f3_wind_speed || '',
                Wind_Direction: c.f3_wind_direction || '',
                Precipitation: c.f3_precipitation || '',
                Torrential_Rain_Rate: c.f3_torrential_rain || '',
                Rainfall_Hourly_mm: c.f3_rainfall_mm || '',
                Holiday_Status: c.f3_holiday || '',
                Ferry_Shift: c.f3_ferry_shift || '',
                ED_Shift: c.f3_ed_shift || '',
                RTN_Book_Ref: c.f3_ref_rtn_book ? 1 : 0,
                RTN_Portal_Ref: c.f3_ref_rtn_portal ? 1 : 0,
                RTN_Search_Date: c.f3_ref_rtn_date || '',
                TMD_Hourly_Ref: c.f3_ref_tmd_hourly ? 1 : 0,
                TMD_Portal_Ref: c.f3_ref_tmd_portal ? 1 : 0,
                TMD_Search_Date: c.f3_ref_tmd_date || ''
            });

            // Form 4 specific
            form4Rows.push({
                STUDY_ID: 'LANTA_' + (c.f4_study_id || id),
                HN_Krabi: c.f4_krabi_hn || '',
                T4_Arrival: (c.f4_t4_date || '') + ' ' + (c.f4_t4_time || ''),
                Admitting_Ward: c.f4_ward || '',
                Attending_Physician: c.f4_physician || '',
                SBP_Krabi: c.f4_sbp || '',
                DBP_Krabi: c.f4_dbp || '',
                MAP_Krabi: c.f4_map || '',
                HR_Krabi: c.f4_hr || '',
                RR_Krabi: c.f4_rr || '',
                SpO2_Krabi: c.f4_spo2 || '',
                BT_Krabi: c.f4_bt || '',
                Hct_Krabi: c.f4_hct || '',
                GCS_E_Krabi: c.f4_gcs_e || '',
                GCS_V_Krabi: c.f4_gcs_v || '',
                GCS_M_Krabi: c.f4_gcs_m || '',
                GCS_Total_Krabi: c.f4_gcs_total || '',
                Killip_Krabi: c.f4_killip || '',
                Stroke_GCS_Krabi: c.f4_stroke_gcs || '',
                Trauma_Acuity_Krabi: c.f4_trauma_acuity || '',
                MSI_Krabi: c.f4_msi || '',
                Delta_Killip: c.f4_eval_killip || '',
                Delta_GCS: c.f4_delta_gcs || '',
                Delta_GCS_Eval: c.f4_eval_gcs || '',
                Delta_RTS: c.f4_delta_rts || '',
                Delta_RTS_Eval: c.f4_eval_rts || '',
                Delta_MSI: c.f4_delta_msi || '',
                Delta_MSI_Eval: c.f4_eval_msi || '',
                Delta_MAP: c.f4_delta_map || '',
                Delta_MAP_Eval: c.f4_eval_map || '',
                Delta_BT: c.f4_delta_bt || '',
                Delta_BT_Eval: c.f4_eval_bt || '',
                Composite_Physiological_Deterioration: c.f4_composite_deter || '',
                T5_Definitive_Care: (c.f4_t5_date || '') + ' ' + (c.f4_t5_time || ''),
                Door_to_Intervention_Krabi_min: c.f4_t4_5_min || '',
                STEMI_Wire_Time: c.f4_pci_wire_time || '',
                STEMI_D2B_min: c.f4_pci_d2b_min || '',
                STEMI_Golden_Window: c.f4_eval_pci || '',
                Stroke_rtPA_Time: c.f4_rtpa_time || '',
                Stroke_O2N_min: c.f4_stroke_o2n_min || '',
                Stroke_Golden_Window: c.f4_eval_stroke || '',
                Trauma_CT_Time: c.f4_trauma_ct_time || '',
                Trauma_D2CT_min: c.f4_trauma_d2ct_min || '',
                Trauma_OR_Time: c.f4_or_time || '',
                Trauma_D2OR_min: c.f4_trauma_d2or_min || '',
                Trauma_Golden_Window: c.f4_eval_trauma || '',
                Mortality_ER_Immediate: c.f4_mort_er || '',
                Mortality_24h_Post: c.f4_mort_24h || '',
                Primary_Cause_of_Death: c.f4_mort_cause || '',
                ICD10_Cause: c.f4_mort_cause_icd || '',
                Cohort_Classification: c.cohort_classification || '',
                Cohort_Exposures: c.cohort_factors || '',
                MicroTimeline_Delay_Count: c.timeline_delay_count !== undefined ? c.timeline_delay_count : '',
                MicroTimeline_Delayed_List: c.timeline_delayed_intervals || '',
                Overall_Referral_Timeliness: c.timeline_overall_status || ''
            });
        });

        // Add Worksheets
        const wsMaster = XLSX.utils.json_to_sheet(masterRows);
        const wsForm1 = XLSX.utils.json_to_sheet(form1Rows);
        const wsForm2 = XLSX.utils.json_to_sheet(form2Rows);
        const wsForm3 = XLSX.utils.json_to_sheet(form3Rows);
        const wsForm4 = XLSX.utils.json_to_sheet(form4Rows);

        XLSX.utils.book_append_sheet(wb, wsMaster, 'Master_Cohort_Dataset');
        XLSX.utils.book_append_sheet(wb, wsForm1, 'Form_1_Island_ED');
        XLSX.utils.book_append_sheet(wb, wsForm2, 'Form_2_MicroTimeline');
        XLSX.utils.book_append_sheet(wb, wsForm3, 'Form_3_Marine_Weather');
        XLSX.utils.book_append_sheet(wb, wsForm4, 'Form_4_Mainland_Care');

        const nowStr = new Date().toISOString().slice(0, 10);
        XLSX.writeFile(wb, 'Emergency_Transfer_CRF_Master_Database_' + nowStr + '.xlsx');
    }

    // --- INDIVIDUAL PATIENT PDF EXPORT ENGINE ---
    let currentPdfTargetId = null;

    function openPdfModal(targetStudyId = null) {
        currentPdfTargetId = targetStudyId || localStorage.getItem('online_crf_last_active_id') || document.getElementById('f1_study_id')?.value.trim() || '001';
        
        // Fetch case info
        const raw = localStorage.getItem('online_crf_case_' + currentPdfTargetId);
        let hn = '';
        let referId = '';
        let nameDetail = '';
        if (raw) {
            try {
                const data = JSON.parse(raw);
                hn = data.f1_hn || '';
                referId = data.f1_refer_id || '';
                const age = data.f1_age ? data.f1_age + ' ปี' : '';
                const sex = data.f1_sex === '1' ? 'ชาย' : data.f1_sex === '2' ? 'หญิง' : '';
                if (age || sex) nameDetail = ' [' + [age, sex].filter(Boolean).join(', ') + ']';
            } catch (e) {}
        }

        const infoEl = document.getElementById('pdf-target-case-info');
        if (infoEl) {
            infoEl.innerHTML = 'ผู้ป่วย: <span style="color:#1e40af; font-size:16px;">LANTA_' + currentPdfTargetId + '</span> ' +
                (hn ? '<span style="color:#475569;">(HN: ' + hn + ')</span> ' : '') +
                (referId ? '<span style="color:#64748b;">[Ref: ' + referId + ']</span>' : '') +
                nameDetail;
        }

        const modal = document.getElementById('pdf-export-modal');
        if (modal) modal.style.display = 'flex';
    }

    function closePdfModal() {
        const modal = document.getElementById('pdf-export-modal');
        if (modal) modal.style.display = 'none';
    }

    function executeExportPDF(allForms = true) {
        // If a specific target ID was set and differs from current active form, load it
        const currentActiveId = localStorage.getItem('online_crf_last_active_id');
        if (currentPdfTargetId && currentPdfTargetId !== currentActiveId) {
            loadCase(currentPdfTargetId);
        }

        closePdfModal();

        // Configure printing mode
        if (allForms) {
            document.body.classList.remove('print-single-tab');
        } else {
            document.body.classList.add('print-single-tab');
        }

        // Set document title so browser uses it as suggested PDF filename
        const activeId = localStorage.getItem('online_crf_last_active_id') || '001';
        const hn = document.getElementById('f1_hn')?.value || '';
        const originalTitle = document.title;
        const reportType = allForms ? 'Complete_Forms_1_to_4' : ('Form_' + currentTab);
        document.title = 'CRF_Patient_Report_LANTA_' + activeId + (hn ? '_HN_' + hn : '') + '_' + reportType;

        // Trigger print after slight timeout to ensure styles apply
        setTimeout(() => {
            window.print();
            // Restore state after print dialog closes
            setTimeout(() => {
                document.title = originalTitle;
                document.body.classList.remove('print-single-tab');
            }, 1000);
        }, 150);
    }

    function adminExportPDF(studyId) {
        openPdfModal(studyId);
    }

    // --- ADMIN DASHBOARD & MANAGEMENT ENGINE ---
    const ADMIN_PIN = '1212312121';

    function openAdminDashboard() {
        const isAuth = sessionStorage.getItem('crf_admin_authorized') === 'true';
        if (isAuth) {
            showAdminDashboardModal();
        } else {
            const modal = document.getElementById('admin-auth-modal');
            const passInput = document.getElementById('admin-password-input');
            const errEl = document.getElementById('admin-auth-error');
            if (modal) {
                if (errEl) errEl.style.display = 'none';
                if (passInput) passInput.value = '';
                modal.style.display = 'flex';
                setTimeout(() => passInput?.focus(), 150);
            }
        }
    }

    function closeAdminAuthModal() {
        const modal = document.getElementById('admin-auth-modal');
        if (modal) modal.style.display = 'none';
    }

    function verifyAdminPassword() {
        const passInput = document.getElementById('admin-password-input');
        const errEl = document.getElementById('admin-auth-error');
        const pass = passInput?.value.trim();

        if (pass === ADMIN_PIN) {
            sessionStorage.setItem('crf_admin_authorized', 'true');
            closeAdminAuthModal();
            showAdminDashboardModal();
        } else {
            if (errEl) errEl.style.display = 'block';
            if (passInput) {
                passInput.focus();
                passInput.select();
            }
        }
    }

    function showAdminDashboardModal() {
        renderAdminDashboard();
        const modal = document.getElementById('admin-dashboard-modal');
        if (modal) modal.style.display = 'flex';
    }

    function closeAdminDashboard() {
        const modal = document.getElementById('admin-dashboard-modal');
        if (modal) modal.style.display = 'none';
    }

    function adminLogout() {
        sessionStorage.removeItem('crf_admin_authorized');
        closeAdminDashboard();
        const statusEl = document.getElementById('save-status');
        if (statusEl) {
            statusEl.innerHTML = '🔒 ออกจากระบบ Admin แล้ว';
            statusEl.style.display = 'inline-flex';
            setTimeout(() => statusEl.style.display = 'none', 3000);
        }
    }

    function renderAdminDashboard() {
        const index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
        const tbody = document.getElementById('admin-cases-tbody');
        if (!tbody) return;

        let totalPatients = index.length;
        let totalTransferMinutes = 0;
        let transferTimeCount = 0;
        let esi1Count = 0;
        let survivalCount = 0;
        let mortalityAssessedCount = 0;

        // Pie Chart Statistics Counters
        let diseaseCounts = { stemi: 0, stroke: 0, trauma: 0, other: 0 };
        let timelinessCounts = { ontime: 0, delay: 0, unknown: 0 };
        let outcomeCounts = { survive: 0, death: 0, pending: 0 };
        let esiCounts = { esi1: 0, esi2: 0, esi3: 0, other: 0 };

        let rowsHtml = '';

        if (index.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 25px; color: #64748b; font-size: 14px;">ยังไม่มีข้อมูลเคสผู้ป่วยในระบบ กดปุ่ม "➕ เคสใหม่" เพื่อเริ่มบันทึก</td></tr>';
        } else {
            index.forEach(studyId => {
                const raw = localStorage.getItem('online_crf_case_' + studyId);
                if (!raw) return;
                let data = {};
                try {
                    data = JSON.parse(raw);
                } catch(e) {
                    return;
                }

                // Calculations for Stats
                const esi = data.f1_esi || data.f1_triage_esi || '';
                if (esi === '1') esi1Count++;
                if (esi === '1') esiCounts.esi1++;
                else if (esi === '2') esiCounts.esi2++;
                else if (esi === '3') esiCounts.esi3++;
                else esiCounts.other++;

                const transferMin = parseFloat(data.f2_t_total_min || data.f2_eq1_total_transfer);
                if (!isNaN(transferMin) && transferMin > 0) {
                    totalTransferMinutes += transferMin;
                    transferTimeCount++;
                    if (transferMin <= 180) timelinessCounts.ontime++;
                    else timelinessCounts.delay++;
                } else {
                    timelinessCounts.unknown++;
                }

                const mortStatus = data.f4_mort_status !== undefined && data.f4_mort_status !== '' ? data.f4_mort_status : (data.f4_mort_24h !== undefined && data.f4_mort_24h !== '' ? data.f4_mort_24h : data.f4_mort_er);
                if (mortStatus !== undefined && mortStatus !== '') {
                    mortalityAssessedCount++;
                    if (mortStatus === '0') {
                        survivalCount++;
                        outcomeCounts.survive++;
                    } else if (mortStatus === '1') {
                        outcomeCounts.death++;
                    } else {
                        outcomeCounts.pending++;
                    }
                } else {
                    outcomeCounts.pending++;
                }

                // Extracted strings
                const displayId = 'LANTA_' + studyId;
                const hn = data.f1_hn || '-';
                const referId = data.f1_refer_id || '-';
                const age = data.f1_age ? data.f1_age + ' ปี' : '-';
                const sex = data.f1_sex === '1' ? 'ชาย' : data.f1_sex === '2' ? 'หญิง' : '-';

                // Triage badge
                let esiBadge = '-';
                if (esi === '1') esiBadge = '<span class="badge-evaluated" style="background:#fee2e2; color:#b91c1c; font-size:11px;">ESI 1</span>';
                else if (esi === '2') esiBadge = '<span class="badge-evaluated" style="background:#ffedd5; color:#c2410c; font-size:11px;">ESI 2</span>';
                else if (esi === '3') esiBadge = '<span class="badge-evaluated" style="background:#fef9c3; color:#a16207; font-size:11px;">ESI 3</span>';
                else if (esi) esiBadge = '<span class="badge-evaluated" style="background:#f1f5f9; color:#475569; font-size:11px;">ESI ' + esi + '</span>';

                // Condition badges
                const isCaseStemi = data.f1_target_disease === 'stemi' || data.f1_inc4_stemi || data.f1_cond_stemi;
                const isCaseStroke = data.f1_target_disease === 'ais' || data.f1_inc4_ais || data.f1_cond_stroke;
                const isCaseTrauma = data.f1_target_disease === 'trauma' || data.f1_inc4_trauma || data.f1_cond_trauma;

                if (isCaseStemi) diseaseCounts.stemi++;
                else if (isCaseStroke) diseaseCounts.stroke++;
                else if (isCaseTrauma) diseaseCounts.trauma++;
                else diseaseCounts.other++;

                const conds = [];
                if (isCaseStemi) conds.push('<span style="background:#fee2e2; color:#991b1b; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:600;">STEMI</span>');
                if (isCaseStroke) conds.push('<span style="background:#fef3c7; color:#92400e; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:600;">Stroke</span>');
                if (isCaseTrauma) conds.push('<span style="background:#ede9fe; color:#5b21b6; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:600;">Trauma</span>');
                if (data.f1_cond_sepsis) conds.push('<span style="background:#e0e7ff; color:#3730a3; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:600;">Sepsis</span>');
                if (data.f1_cond_arrest) conds.push('<span style="background:#fce7f3; color:#9d174d; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:600;">Cardiac Arrest</span>');
                if (data.f1_cond_other && data.f1_cond_other_specify) {
                    conds.push('<span style="background:#f1f5f9; color:#475569; padding:1px 6px; border-radius:4px; font-size:11px;">' + data.f1_cond_other_specify + '</span>');
                }
                const condHtml = conds.length > 0 ? conds.join(' ') : '<span style="color:#94a3b8;">-</span>';

                // Transfer time
                let transferHtml = '-';
                if (!isNaN(transferMin) && transferMin > 0) {
                    const isDelay = transferMin > 180;
                    transferHtml = '<b>' + transferMin + '</b> น. ' + (isDelay ? '<span class="badge-evaluated badge-delay" style="font-size:10px;">ล่าช้า</span>' : '<span class="badge-evaluated badge-ontime" style="font-size:10px;">ตามเกณฑ์</span>');
                }

                // RTS
                let rtsHtml = '-';
                if (isCaseTrauma) {
                    const rts1 = data.f1_rts_total || '-';
                    const rts4 = data.f4_rts_total || '-';
                    rtsHtml = rts1 + ' ➔ ' + rts4;
                } else if (isCaseStroke) {
                    rtsHtml = '<span style="color:#94a3b8; font-size:11px;">(Stroke: N/A)</span>';
                } else if (isCaseStemi) {
                    rtsHtml = '<span style="color:#94a3b8; font-size:11px;">(STEMI: N/A)</span>';
                }

                // Outcome
                let outcomeHtml = '<span style="color:#94a3b8;">รอผล</span>';
                if (mortStatus === '0') {
                    outcomeHtml = '<span class="badge-evaluated badge-ontime" style="background:#dcfce7; color:#15803d; font-size:11px;">✓ รอดชีวิต</span>';
                } else if (mortStatus === '1') {
                    outcomeHtml = '<span class="badge-evaluated badge-delay" style="background:#fee2e2; color:#b91c1c; font-size:11px;">✕ เสียชีวิต</span>';
                }

                rowsHtml += `
                    <tr class="admin-case-row" data-id="${studyId}" data-hn="${hn}" data-refer="${referId}" data-esi="${esi}">
                        <td style="text-align: center; font-weight: 700; color: #1e40af;">${displayId}</td>
                        <td>
                            <div><b>HN:</b> ${hn}</div>
                            <div style="font-size: 11.5px; color: #64748b;"><b>Ref:</b> ${referId}</div>
                        </td>
                        <td style="text-align: center;">${age} / ${sex}</td>
                        <td style="text-align: center;">${esiBadge}</td>
                        <td>${condHtml}</td>
                        <td style="text-align: center;">${transferHtml}</td>
                        <td style="text-align: center; font-size: 12.5px;">${rtsHtml}</td>
                        <td style="text-align: center;">${outcomeHtml}</td>
                        <td style="text-align: center;">
                            <div style="display: flex; gap: 4px; justify-content: center;">
                                <button type="button" class="btn btn-outline" style="padding: 3px 7px; font-size: 11.5px;" onclick="adminViewCase('${studyId}')" title="เปิดดูหรือแก้ไขเคสนี้">
                                    ✏️ ดู/แก้ไข
                                </button>
                                <button type="button" class="btn btn-outline" style="padding: 3px 7px; font-size: 11.5px; color: #1e40af; border-color: #93c5fd;" onclick="adminExportPDF('${studyId}')" title="ส่งออกรายงานข้อมูลคนไข้รายนี้เป็น PDF หรือสั่งพิมพ์">
                                    📄 PDF
                                </button>
                                <button type="button" class="btn btn-outline" style="padding: 3px 7px; font-size: 11.5px; color: #b91c1c; border-color: #fca5a5;" onclick="adminDeleteCase('${studyId}')" title="ลบเคสนี้ออกจากฐานข้อมูล">
                                    🗑️ ลบ
                                </button>
                            </div>
                        </td>
                    </tr>
                `;
            });
            tbody.innerHTML = rowsHtml;
        }

        // Update Stat Cards
        const statTotal = document.getElementById('stat-total-patients');
        if (statTotal) statTotal.textContent = totalPatients;

        const statMean = document.getElementById('stat-mean-time');
        const statDetail = document.getElementById('stat-time-detail');
        if (statMean) {
            const avg = transferTimeCount > 0 ? (totalTransferMinutes / transferTimeCount).toFixed(1) : '0';
            statMean.innerHTML = avg + ' <span style="font-size: 14px; font-weight: 500;">นาที</span>';
        }
        if (statDetail) {
            statDetail.textContent = 'คำนวณจาก ' + transferTimeCount + ' เคส';
        }

        const statEsi1 = document.getElementById('stat-esi1-count');
        const statEsiPct = document.getElementById('stat-esi1-pct');
        if (statEsi1) statEsi1.textContent = esi1Count;
        if (statEsiPct) {
            const pct = totalPatients > 0 ? ((esi1Count / totalPatients) * 100).toFixed(1) : '0';
            statEsiPct.textContent = pct + '% ของผู้ป่วยทั้งหมด';
        }

        const statSurv = document.getElementById('stat-survival-rate');
        const statSurvDetail = document.getElementById('stat-survival-detail');
        if (statSurv) {
            const survPct = mortalityAssessedCount > 0 ? ((survivalCount / mortalityAssessedCount) * 100).toFixed(1) : '-';
            statSurv.textContent = survPct !== '-' ? survPct + '%' : '-';
        }
        if (statSurvDetail) {
            statSurvDetail.textContent = 'รอดชีวิต ' + survivalCount + ' / ประเมิน ' + mortalityAssessedCount + ' เคส';
        }

        // Render 4 Clinical Research Donut / Pie Charts
        renderDonutChart('pie-chart-disease', 'pie-center-disease', 'pie-legend-disease', [
            { label: 'STEMI', count: diseaseCounts.stemi, color: '#dc2626' },
            { label: 'Stroke', count: diseaseCounts.stroke, color: '#d97706' },
            { label: 'Trauma', count: diseaseCounts.trauma, color: '#7c3aed' },
            { label: 'อื่นๆ/ไม่ระบุ', count: diseaseCounts.other, color: '#94a3b8' }
        ], totalPatients, 'เคส');

        const timeKnownTotal = timelinessCounts.ontime + timelinessCounts.delay;
        const ontimePct = timeKnownTotal > 0 ? Math.round((timelinessCounts.ontime / timeKnownTotal) * 100) + '%' : '0%';
        renderDonutChart('pie-chart-timeliness', 'pie-center-timeliness', 'pie-legend-timeliness', [
            { label: 'ทันเกณฑ์ (≤3ชม.)', count: timelinessCounts.ontime, color: '#059669' },
            { label: 'ล่าช้า (>3ชม.)', count: timelinessCounts.delay, color: '#e11d48' },
            { label: 'รอเวลาครบ', count: timelinessCounts.unknown, color: '#cbd5e1' }
        ], ontimePct, 'ทันเกณฑ์');

        const survTotal = outcomeCounts.survive + outcomeCounts.death;
        const survPct = survTotal > 0 ? Math.round((outcomeCounts.survive / survTotal) * 100) + '%' : '-';
        renderDonutChart('pie-chart-survival', 'pie-center-survival', 'pie-legend-survival', [
            { label: 'รอดชีวิต 24 ชม.', count: outcomeCounts.survive, color: '#16a34a' },
            { label: 'เสียชีวิต', count: outcomeCounts.death, color: '#dc2626' },
            { label: 'รอผล/ติดตาม', count: outcomeCounts.pending, color: '#f59e0b' }
        ], survPct, 'รอดชีวิต');

        renderDonutChart('pie-chart-esi', 'pie-center-esi', 'pie-legend-esi', [
            { label: 'ESI 1 (กู้ชีพ)', count: esiCounts.esi1, color: '#991b1b' },
            { label: 'ESI 2 (ฉุกเฉินมาก)', count: esiCounts.esi2, color: '#ea580c' },
            { label: 'ESI 3 (ปานกลาง)', count: esiCounts.esi3, color: '#ca8a04' },
            { label: 'ESI 4-5/อื่นๆ', count: esiCounts.other, color: '#64748b' }
        ], totalPatients, 'เคส');
    }

    function renderDonutChart(chartId, centerId, legendId, slices, centerText, centerLabel) {
        const chartEl = document.getElementById(chartId);
        const centerEl = document.getElementById(centerId);
        const legendEl = document.getElementById(legendId);
        if (!chartEl || !legendEl) return;

        const total = slices.reduce((sum, s) => sum + s.count, 0);
        if (total === 0) {
            chartEl.style.background = '#e2e8f0';
            if (centerEl) centerEl.textContent = '0';
            legendEl.innerHTML = '<div style="color:#94a3b8; font-size:11px; text-align:center; padding:10px 0;">ยังไม่มีข้อมูล</div>';
            return;
        }

        let currentPct = 0;
        const gradientParts = [];
        let legendHtml = '<div style="display:flex; flex-direction:column; gap:3px; font-size:11px; width:100%;">';

        slices.forEach(s => {
            if (s.count <= 0) return;
            const pct = (s.count / total) * 100;
            const nextPct = currentPct + pct;
            gradientParts.push(`${s.color} ${currentPct.toFixed(1)}% ${nextPct.toFixed(1)}%`);
            currentPct = nextPct;

            legendHtml += `
                <div style="display:flex; justify-content:space-between; align-items:center; gap:4px;">
                    <div style="display:flex; align-items:center; gap:4px; min-width:0; overflow:hidden;">
                        <span style="width:7px; height:7px; border-radius:50%; background:${s.color}; flex-shrink:0;"></span>
                        <span style="color:#334155; font-weight:500; white-space:nowrap; text-overflow:ellipsis; overflow:hidden; font-size:10.5px;">${s.label}</span>
                    </div>
                    <div style="font-weight:700; color:#0f172a; white-space:nowrap; font-size:10.5px;">
                        ${s.count} <span style="font-size:9.5px; color:#64748b; font-weight:normal;">(${pct.toFixed(0)}%)</span>
                    </div>
                </div>`;
        });
        legendHtml += '</div>';

        chartEl.style.background = `conic-gradient(${gradientParts.join(', ')})`;
        if (centerEl) centerEl.textContent = centerText !== undefined ? centerText : total;
        legendEl.innerHTML = legendHtml;
    }

    function filterAdminCases() {
        const query = (document.getElementById('admin-search-box')?.value || '').toLowerCase().trim();
        const esiFilter = document.getElementById('admin-esi-filter')?.value || '';

        const rows = document.querySelectorAll('.admin-case-row');
        rows.forEach(row => {
            const id = (row.getAttribute('data-id') || '').toLowerCase();
            const hn = (row.getAttribute('data-hn') || '').toLowerCase();
            const refer = (row.getAttribute('data-refer') || '').toLowerCase();
            const esi = row.getAttribute('data-esi') || '';
            const rowText = row.textContent.toLowerCase();

            const matchQuery = !query || id.includes(query) || hn.includes(query) || refer.includes(query) || rowText.includes(query);
            const matchEsi = !esiFilter || esi === esiFilter;

            if (matchQuery && matchEsi) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    function adminViewCase(studyId) {
        loadCase(studyId);
        closeAdminDashboard();
        switchTab(1);
        const statusEl = document.getElementById('save-status');
        if (statusEl) {
            statusEl.innerHTML = '✓ โหลดเคส LANTA_' + studyId + ' เพื่อตรวจสอบ/แก้ไขเรียบร้อยแล้ว';
            statusEl.style.display = 'inline-flex';
            setTimeout(() => statusEl.style.display = 'none', 3500);
        }
    }

    function adminDeleteCase(studyId) {
        if (!confirm('⚠️ ยืนยันการลบเคสผู้ป่วย LANTA_' + studyId + ' ออกจากระบบใช่หรือไม่?\\n\\nข้อมูลของเคสนี้จะถูกลบถาวรและไม่สามารถกู้คืนได้')) {
            return;
        }

        // Delete from localStorage
        localStorage.removeItem('online_crf_case_' + studyId);

        // Remove from index
        let index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
        index = index.filter(id => id !== studyId);
        localStorage.setItem('online_crf_case_index', JSON.stringify(index));

        // If active case was deleted
        const curActive = localStorage.getItem('online_crf_last_active_id');
        if (curActive === studyId) {
            if (index.length > 0) {
                loadCase(index[0]);
            } else {
                createNewCase();
            }
        }

        loadCaseIndex();
        renderAdminDashboard();

        alert('✓ ลบข้อมูลเคส LANTA_' + studyId + ' เรียบร้อยแล้ว');
    }
    """
