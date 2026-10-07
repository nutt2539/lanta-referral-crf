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
        toggleIntubationDetails();
        toggleInotropesDetails();

        // Listen for pre-transfer interventions change events
        document.addEventListener('change', function(e) {
            if (e.target && e.target.name === 'f1_intubation') {
                toggleIntubationDetails();
                scheduleAutoSave();
            }
            if (e.target && e.target.name === 'f1_inotropes') {
                toggleInotropesDetails();
                scheduleAutoSave();
            }
        });
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
                alert('⚠️ แจ้งเตือน: ในเกณฑ์การคัดเข้าข้อ 4 บังคับต้องเลือก 1 ใน 3 กลุ่มโรคเป้าหมาย\\n(1. STEMI / ACS, 2. Acute Stroke หรือ 3. Severe Trauma)\\n\\nกรุณาติ๊กเลือกกลุ่มโรคก่อนดำเนินการต่อไป');
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

    // --- Screening Exclusion & Form Locking Engine ---
    function isCaseExcluded() {
        const inc1 = document.querySelector('input[name="f1_inc1"]:checked')?.value;
        const inc2 = document.querySelector('input[name="f1_inc2"]:checked')?.value;
        const inc3 = document.querySelector('input[name="f1_inc3"]:checked')?.value;
        const inc4 = document.querySelector('input[name="f1_inc4"]:checked')?.value;

        const exc1 = document.querySelector('input[name="f1_exc1"]:checked')?.value;
        const exc2 = document.querySelector('input[name="f1_exc2"]:checked')?.value;
        const exc3 = document.querySelector('input[name="f1_exc3"]:checked')?.value;
        const exc4 = document.querySelector('input[name="f1_exc4"]:checked')?.value;

        const isIncAnyNo = (inc1 === 'no' || inc2 === 'no' || inc3 === 'no' || inc4 === 'no');
        const isExcAnyYes = (exc1 === 'yes' || exc2 === 'yes' || exc3 === 'yes' || exc4 === 'yes');

        return Boolean(isIncAnyNo || isExcAnyYes);
    }

    function applyScreeningLock(isExcluded) {
        // 1. Lock all controls in Form 1 post-screening sections (Demographics, Vitals, DIDO, etc.)
        const f1PostScreen = document.getElementById('f1_post_screening_container');
        if (f1PostScreen) {
            f1PostScreen.querySelectorAll('input, select, textarea, button').forEach(el => {
                el.disabled = isExcluded;
            });
            f1PostScreen.style.opacity = isExcluded ? '0.45' : '1';
            f1PostScreen.style.pointerEvents = isExcluded ? 'none' : 'auto';
            f1PostScreen.style.userSelect = isExcluded ? 'none' : 'auto';
        }
        const f1LockAlert = document.getElementById('f1_excluded_lock_alert');
        if (f1LockAlert) f1LockAlert.style.display = isExcluded ? 'block' : 'none';

        // 2. Lock all controls in Form 2, Form 3, Form 4
        ['page-form2', 'page-form3', 'page-form4'].forEach(pageId => {
            const pageEl = document.getElementById(pageId);
            if (pageEl) {
                pageEl.querySelectorAll('input, select, textarea').forEach(el => {
                    el.disabled = isExcluded;
                });
                pageEl.style.opacity = isExcluded ? '0.45' : '1';
                pageEl.style.pointerEvents = isExcluded ? 'none' : 'auto';
            }
        });

        // 3. Form 2, 3, 4 banner alerts
        document.querySelectorAll('.form-excluded-lock-banner').forEach(el => {
            el.style.display = isExcluded ? 'block' : 'none';
        });

        // 4. Tab bar styling for Tabs 2, 3, 4
        [2, 3, 4].forEach(tabNum => {
            const btn = document.getElementById('tab-btn-' + tabNum);
            if (btn) {
                btn.style.opacity = isExcluded ? '0.45' : '1';
                btn.style.cursor = isExcluded ? 'not-allowed' : 'pointer';
                btn.title = isExcluded ? 'ปิดกั้นการเข้าถึง (เคสไม่ผ่านเกณฑ์การคัดกรอง)' : '';
            }
        });

        // 5. Update bottom nav bar
        updateBottomNav();
    }

    // --- Tab Navigation ---
    function switchTab(tabIndex) {
        tabIndex = Number(tabIndex);
        if (tabIndex > 1) {
            if (isCaseExcluded()) {
                alert('⛔ ไม่สามารถเปิดส่วนที่ ' + tabIndex + ' ได้\\n\\nเคสนี้ไม่ผ่านเกณฑ์การคัดกรอง (Excluded Case) ระบบจึงปิดกั้นการบันทึกข้อมูลใน Form 2–4\\n\\nหากต้องการแก้ไขผลการคัดกรอง กรุณากลับไปตรวจสอบคำตอบในเกณฑ์การคัดเข้า/คัดออกในส่วนที่ 1');
                return;
            }
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

        const isExcluded = isCaseExcluded();

        if (currentTab === 1) {
            prevBtn.style.visibility = 'hidden';
            if (isExcluded) {
                nextBtn.disabled = true;
                nextBtn.className = 'btn btn-outline';
                nextBtn.style.opacity = '0.5';
                nextBtn.style.cursor = 'not-allowed';
                nextBtn.innerHTML = '🔒 ปิดกั้นการดำเนินการ (เคสไม่ผ่านเกณฑ์)';
            } else {
                nextBtn.disabled = false;
                nextBtn.className = 'btn btn-theme-2';
                nextBtn.style.opacity = '1';
                nextBtn.style.cursor = 'pointer';
                nextBtn.innerHTML = '<span>ถัดไป: ส่วนที่ 2 (Form 2) ➔</span>';
            }
        } else if (currentTab === 2) {
            prevBtn.style.visibility = 'visible';
            prevBtn.innerHTML = '⬅ ย้อนกลับไปส่วนที่ 1 (Form 1)';
            nextBtn.className = 'btn btn-theme-3';
            nextBtn.disabled = false;
            nextBtn.style.opacity = '1';
            nextBtn.style.cursor = 'pointer';
            nextBtn.innerHTML = '<span>ถัดไป: ส่วนที่ 3 (Form 3) ➔</span>';
        } else if (currentTab === 3) {
            prevBtn.style.visibility = 'visible';
            prevBtn.innerHTML = '⬅ ย้อนกลับไปส่วนที่ 2 (Form 2)';
            nextBtn.className = 'btn btn-theme-4';
            nextBtn.disabled = false;
            nextBtn.style.opacity = '1';
            nextBtn.style.cursor = 'pointer';
            nextBtn.innerHTML = '<span>ถัดไป: ส่วนที่ 4 (Form 4) ➔</span>';
        } else if (currentTab === 4) {
            prevBtn.style.visibility = 'visible';
            prevBtn.innerHTML = '⬅ ย้อนกลับไปส่วนที่ 3 (Form 3)';
            nextBtn.className = 'btn btn-blue';
            nextBtn.disabled = false;
            nextBtn.style.opacity = '1';
            nextBtn.style.cursor = 'pointer';
            nextBtn.innerHTML = '<span>💾 บันทึกข้อมูลเคสนี้</span>';
        }
    }

    function nextTab() {
        if (currentTab === 1) {
            if (isCaseExcluded()) {
                alert('⛔ ไม่สามารถดำเนินการต่อได้\\n\\nเคสนี้ไม่ผ่านเกณฑ์การคัดกรอง (Excluded Case) ระบบจึงปิดกั้นการบันทึกข้อมูลใน Form 2–4');
                return;
            }
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
                alert('⚠️ ในเกณฑ์การคัดเข้าข้อ 4 บังคับต้องเลือก 1 ใน 3 กลุ่มโรคเป้าหมาย\\n(1. STEMI / ACS, 2. Acute Stroke หรือ 3. Severe Trauma)\\n\\nกรุณาคลิกเลือกกลุ่มโรคทางด้านซ้าย');
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
            else if (disease === 'ais') dName = '2. Acute Stroke';
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

    // --- Pre-Transfer Intubation ETT Gating ---
    function toggleIntubationDetails() {
        const rad = document.querySelector('input[name="f1_intubation"]:checked');
        const isIntub = (rad && rad.value === '1');
        const box = document.getElementById('f1_ett_details_box');
        const ettNo = document.getElementById('f1_ett_no');
        const ettTime = document.getElementById('f1_ett_time');

        if (box) {
            if (isIntub) {
                box.style.opacity = '1';
                box.style.pointerEvents = 'auto';
                if (ettNo) {
                    ettNo.disabled = false;
                    ettNo.style.backgroundColor = '#ffffff';
                }
                if (ettTime) {
                    ettTime.disabled = false;
                    ettTime.style.backgroundColor = '#ffffff';
                }
            } else {
                box.style.opacity = '0.35';
                box.style.pointerEvents = 'none';
                if (ettNo) {
                    ettNo.disabled = true;
                    ettNo.value = '';
                    ettNo.style.backgroundColor = '#f1f5f9';
                }
                if (ettTime) {
                    ettTime.disabled = true;
                    ettTime.value = '';
                    ettTime.style.backgroundColor = '#f1f5f9';
                }
            }
        }
    }

    // --- Pre-Transfer Inotropes Gating ---
    function toggleInotropesDetails() {
        const rad = document.querySelector('input[name="f1_inotropes"]:checked');
        const isInot = (rad && rad.value === '1');
        const box = document.getElementById('f1_inotropes_details_box');
        const inotName = document.getElementById('f1_inotropes_name');
        const inotDose = document.getElementById('f1_inotropes_dose');

        if (box) {
            if (isInot) {
                box.style.opacity = '1';
                box.style.pointerEvents = 'auto';
                if (inotName) {
                    inotName.disabled = false;
                    inotName.style.backgroundColor = '#ffffff';
                }
                if (inotDose) {
                    inotDose.disabled = false;
                    inotDose.style.backgroundColor = '#ffffff';
                }
            } else {
                box.style.opacity = '0.35';
                box.style.pointerEvents = 'none';
                if (inotName) {
                    inotName.disabled = true;
                    inotName.value = '';
                    inotName.style.backgroundColor = '#f1f5f9';
                }
                if (inotDose) {
                    inotDose.disabled = true;
                    inotDose.value = '';
                    inotDose.style.backgroundColor = '#f1f5f9';
                }
            }
        }
    }

    if (typeof window !== 'undefined') {
        window.toggleIntubationDetails = toggleIntubationDetails;
        window.toggleInotropesDetails = toggleInotropesDetails;
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
        if (f4_d) f4_d.value = d || '';
        if (f4_t) f4_t.value = t || '';
        if (typeof calcForm2Timelines === 'function') calcForm2Timelines();
        if (typeof calcForm4Timelines === 'function') calcForm4Timelines();
    }

    function syncT4_fromF4() {
        const d = document.getElementById('f4_t4_date')?.value;
        const t = document.getElementById('f4_t4_time')?.value;
        const f2_d = document.getElementById('f2_t4_date');
        const f2_t = document.getElementById('f2_t4_time');
        if (f2_d) f2_d.value = d || '';
        if (f2_t) f2_t.value = t || '';
        if (typeof calcForm2Timelines === 'function') calcForm2Timelines();
        if (typeof calcForm4Timelines === 'function') calcForm4Timelines();
    }

    let isSyncingT5 = false;

    function syncT5() {
        if (isSyncingT5) return;
        isSyncingT5 = true;
        try {
            let d = document.getElementById('f2_t5_date')?.value;
            const t = document.getElementById('f2_t5_time')?.value;
            const f4_d = document.getElementById('f4_t5_date');
            const f4_t = document.getElementById('f4_t5_time');

            // Fallback date if user only entered time
            if (!d && t) {
                d = document.getElementById('f4_t5_date')?.value ||
                    document.getElementById('f2_t4_date')?.value ||
                    document.getElementById('f4_t4_date')?.value ||
                    document.getElementById('f1_t0_date')?.value || '';
                const f2_d = document.getElementById('f2_t5_date');
                if (f2_d && d) f2_d.value = d;
            }

            if (f4_d) f4_d.value = d || '';
            if (f4_t) f4_t.value = t || '';

            // Auto-fill disease specific intervention in Form 4 if empty
            const isStemi = document.getElementById('f1_inc4_stemi')?.checked;
            const isStroke = document.getElementById('f1_inc4_ais')?.checked;
            if (isStemi && t) {
                const pciWire = document.getElementById('f4_pci_wire_time');
                if (pciWire && !pciWire.value) pciWire.value = t;
            } else if (isStroke && t) {
                const rtpa = document.getElementById('f4_rtpa_time');
                if (rtpa && !rtpa.value) rtpa.value = t;
            }

            if (typeof calcForm2Timelines === 'function') calcForm2Timelines();
            if (typeof calcForm4Timelines === 'function') calcForm4Timelines();
        } finally {
            isSyncingT5 = false;
        }
    }

    function syncT5_fromF4() {
        if (isSyncingT5) return;
        isSyncingT5 = true;
        try {
            let d = document.getElementById('f4_t5_date')?.value;
            const t = document.getElementById('f4_t5_time')?.value;
            const f2_d = document.getElementById('f2_t5_date');
            const f2_t = document.getElementById('f2_t5_time');

            // Fallback date if user only entered time
            if (!d && t) {
                d = document.getElementById('f2_t5_date')?.value ||
                    document.getElementById('f4_t4_date')?.value ||
                    document.getElementById('f2_t4_date')?.value ||
                    document.getElementById('f1_t0_date')?.value || '';
                const f4_d = document.getElementById('f4_t5_date');
                if (f4_d && d) f4_d.value = d;
            }

            if (f2_d) f2_d.value = d || '';
            if (f2_t) f2_t.value = t || '';

            // Auto-fill disease specific intervention in Form 4 if empty
            const isStemi = document.getElementById('f1_inc4_stemi')?.checked;
            const isStroke = document.getElementById('f1_inc4_ais')?.checked;
            if (isStemi && t) {
                const pciWire = document.getElementById('f4_pci_wire_time');
                if (pciWire && !pciWire.value) pciWire.value = t;
            } else if (isStroke && t) {
                const rtpa = document.getElementById('f4_rtpa_time');
                if (rtpa && !rtpa.value) rtpa.value = t;
            }

            if (typeof calcForm2Timelines === 'function') calcForm2Timelines();
            if (typeof calcForm4Timelines === 'function') calcForm4Timelines();
        } finally {
            isSyncingT5 = false;
        }
    }

    function syncT5_fromIntervention(type) {
        let t = '';
        if (type === 'stemi') {
            t = document.getElementById('f4_pci_wire_time')?.value;
        } else if (type === 'ais') {
            t = document.getElementById('f4_rtpa_time')?.value;
        } else if (type === 'trauma_or') {
            t = document.getElementById('f4_or_time')?.value;
        } else if (type === 'trauma_ct') {
            const orTime = document.getElementById('f4_or_time')?.value;
            const currentT5 = document.getElementById('f4_t5_time')?.value;
            if (!orTime && !currentT5) {
                t = document.getElementById('f4_trauma_ct_time')?.value;
            } else {
                return;
            }
        }
        if (t !== undefined) {
            const f4_t = document.getElementById('f4_t5_time');
            if (f4_t) f4_t.value = t;
            syncT5_fromF4();
        }
    }

    function syncT5_bidirectional() {
        const f2_d = document.getElementById('f2_t5_date')?.value;
        const f2_t = document.getElementById('f2_t5_time')?.value;
        const f4_d = document.getElementById('f4_t5_date')?.value;
        const f4_t = document.getElementById('f4_t5_time')?.value;

        if (f2_t && !f4_t) {
            syncT5();
        } else if (f4_t && !f2_t) {
            syncT5_fromF4();
        } else if (f2_t && f4_t) {
            if (f2_d && !f4_d) {
                const el = document.getElementById('f4_t5_date');
                if (el) el.value = f2_d;
            } else if (f4_d && !f2_d) {
                const el = document.getElementById('f2_t5_date');
                if (el) el.value = f4_d;
            }
        }
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

        const reasons = [];
        if (inc1 === 'no') reasons.push('เกณฑ์คัดเข้าข้อ 1: ระยะเวลาส่งต่อนอกช่วง 1 ม.ค. 2564 – 31 ธ.ค. 2569');
        if (inc2 === 'no') reasons.push('เกณฑ์คัดเข้าข้อ 2: ผู้ป่วยอายุต่ำกว่า 18 ปีบริบูรณ์ (ไม่ใช่ผู้ป่วยผู้ใหญ่)');
        if (inc3 === 'no') reasons.push('เกณฑ์คัดเข้าข้อ 3: ไม่มีเอกสารการส่งต่อ หรือไม่ได้ส่งต่อผ่านทางรถพยาบาลและแพขนานยนต์');
        if (inc4 === 'no') reasons.push('เกณฑ์คัดเข้าข้อ 4: ไม่ได้เป็นผู้ป่วยฉุกเฉินระดับ ESI 1–2 ใน 3 กลุ่มโรคเป้าหมาย');

        if (exc1 === 'yes') reasons.push('เกณฑ์คัดออกข้อ 1: เสียชีวิตก่อนนำส่งหรือเสียชีวิตก่อนเคลื่อนย้ายออกจาก รพ.เกาะลันตา (DOA / Deceased before transfer)');
        if (exc2 === 'yes') reasons.push('เกณฑ์คัดออกข้อ 2: ส่งต่อด้วยอากาศยานทางการแพทย์ (Sky doctor / HEMS)');
        if (exc3 === 'yes') reasons.push('เกณฑ์คัดออกข้อ 3: ปฏิเสธการส่งต่อ / ขอย้ายไปเอง (Refused transfer / DAMA)');
        if (exc4 === 'yes') reasons.push('เกณฑ์คัดออกข้อ 4: ข้อมูลระบุเวลาของผลลัพธ์ปฐมภูมิไม่ครบถ้วน (Missing essential timestamps)');

        const isIncAllYes = (inc1 === 'yes' && inc2 === 'yes' && inc3 === 'yes' && inc4 === 'yes' && Boolean(disease));
        const isExcAllNo = (exc1 === 'no' && exc2 === 'no' && exc3 === 'no' && exc4 === 'no');

        const isExcluded = (reasons.length > 0);
        const isEligible = (!isExcluded && isIncAllYes && isExcAllNo);

        // Elements
        const card = document.getElementById('screening_summary_card');
        const iconBadge = document.getElementById('screening_icon_badge');
        const pill = document.getElementById('screening_status_pill');
        const lockIndicator = document.getElementById('screening_lock_indicator');
        const desc = document.getElementById('screening_status_desc');
        const badge = document.getElementById('screening_badge');
        const eligYesRadio = document.getElementById('f1_eligible_yes');
        const eligNoRadio = document.getElementById('f1_eligible_no');

        if (badge) badge.style.display = 'none';

        if (isExcluded) {
            if (eligNoRadio) eligNoRadio.checked = true;
            if (eligYesRadio) eligYesRadio.checked = false;

            if (card) {
                card.style.background = '#fef2f2';
                card.style.border = '2px solid #dc2626';
                card.style.boxShadow = '0 1px 6px rgba(220, 38, 38, 0.12)';
            }
            if (iconBadge) iconBadge.innerHTML = '🔴';
            if (pill) {
                pill.style.background = '#dc2626';
                pill.style.color = '#ffffff';
                pill.innerHTML = '✕ ไม่ผ่านเกณฑ์ (Excluded)';
            }
            if (lockIndicator) {
                lockIndicator.innerHTML = '<span style="color: #dc2626; background: #fee2e2; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 11.5px;">🔒 ปิดกั้นการกรอกข้อมูล</span>';
            }
            if (desc) {
                const reasonStr = reasons.length > 0 ? reasons.join('; ') : 'ผู้ป่วยไม่เข้าเกณฑ์การคัดกรอง';
                desc.innerHTML = '<span style="color: #991b1b; font-weight: 600;">⛔ ไม่ผ่านเกณฑ์การศึกษา (' + reasonStr + ') — แบบบันทึกส่วนอื่นๆ ถูกล็อกทั้งหมด</span>';
            }

            applyScreeningLock(true);
        } else if (isEligible) {
            if (eligYesRadio) eligYesRadio.checked = true;
            if (eligNoRadio) eligNoRadio.checked = false;

            if (card) {
                card.style.background = '#ecfdf5';
                card.style.border = '2px solid #10b981';
                card.style.boxShadow = '0 1px 6px rgba(16, 185, 129, 0.12)';
            }
            if (iconBadge) iconBadge.innerHTML = '🟢';
            if (pill) {
                pill.style.background = '#059669';
                pill.style.color = '#ffffff';
                pill.innerHTML = '✓ ผ่านเกณฑ์การวิจัย (Eligible Cohort)';
            }
            if (lockIndicator) {
                lockIndicator.innerHTML = '<span style="color: #047857; background: #dcfce7; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 11.5px;">🔓 ปลดล็อกระบบพร้อมบันทึก</span>';
            }
            let diseaseName = 'ยังไม่ระบุ';
            if (disease === 'stemi') diseaseName = 'STEMI / ACS';
            else if (disease === 'ais') diseaseName = 'Acute Stroke';
            else if (disease === 'trauma') diseaseName = 'Severe Trauma';

            if (desc) {
                desc.innerHTML = '<span style="color: #065f46;">✓ ผู้ป่วยผ่านเกณฑ์คัดเข้าครบถ้วน (กลุ่มโรค: <strong>' + diseaseName + '</strong>) และไม่เข้าเกณฑ์คัดออก — บันทึกข้อมูลส่วนอื่นๆ ได้ตามปกติ</span>';
            }

            applyScreeningLock(false);
        } else {
            // Pending state
            if (eligYesRadio) eligYesRadio.checked = false;
            if (eligNoRadio) eligNoRadio.checked = false;

            if (card) {
                card.style.background = '#f8fafc';
                card.style.border = '1.5px dashed #94a3b8';
                card.style.boxShadow = 'none';
            }
            if (iconBadge) iconBadge.innerHTML = '⚖️';
            if (pill) {
                pill.style.background = '#e2e8f0';
                pill.style.color = '#475569';
                pill.innerHTML = '⏳ รอการประเมินเกณฑ์';
            }
            if (lockIndicator) {
                lockIndicator.innerHTML = '<span style="color: #64748b; font-size: 11.5px;">รอประเมินเกณฑ์</span>';
            }
            if (desc) {
                desc.innerHTML = '<span style="color: #64748b;">กรุณาตอบเกณฑ์การคัดเข้า (Inclusion 4 ข้อ) และเกณฑ์การคัดออก (Exclusion 4 ข้อ) ด้านบนให้ครบถ้วนเพื่อประเมินอัตโนมัติ</span>';
            }

            applyScreeningLock(false);
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
            const curTot = parseInt(document.getElementById('f1_gcs_total')?.value, 10);
            if (!isNaN(curTot)) {
                const isStroke = document.getElementById('f1_inc4_ais')?.checked;
                if (isStroke) {
                    if (curTot >= 3 && curTot <= 8) {
                        const r1 = document.getElementById('f1_stroke_gcs_1'); if (r1) r1.checked = true;
                    } else if (curTot >= 9 && curTot <= 12) {
                        const r2 = document.getElementById('f1_stroke_gcs_2'); if (r2) r2.checked = true;
                    } else if (curTot >= 13 && curTot <= 15) {
                        const r3 = document.getElementById('f1_stroke_gcs_3'); if (r3) r3.checked = true;
                    }
                }
            } else {
                document.getElementById('f1_gcs_total').value = '';
            }
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
        let t5Date = document.getElementById('f2_t5_date')?.value || document.getElementById('f4_t5_date')?.value;
        let t5Time = document.getElementById('f2_t5_time')?.value || document.getElementById('f4_t5_time')?.value;
        if (!document.getElementById('f2_t5_date')?.value && t5Date) {
            const el = document.getElementById('f2_t5_date');
            if (el) el.value = t5Date;
        }
        if (!document.getElementById('f2_t5_time')?.value && t5Time) {
            const el = document.getElementById('f2_t5_time');
            if (el) el.value = t5Time;
        }

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

        // Auto sync to Form 2 inputs if empty
        const f2_t5_d = document.getElementById('f2_t5_date');
        const f2_t5_t = document.getElementById('f2_t5_time');
        if (f2_t5_d && !f2_t5_d.value && t5Date) f2_t5_d.value = t5Date;
        if (f2_t5_t && !f2_t5_t.value && t5Time) f2_t5_t.value = t5Time;

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
            if (wireTime && !document.getElementById('f4_t5_time')?.value) {
                const f4_t5_t = document.getElementById('f4_t5_time');
                if (f4_t5_t) {
                    f4_t5_t.value = wireTime;
                    syncT5_fromF4();
                }
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
            if (rtpaTime && !document.getElementById('f4_t5_time')?.value) {
                const f4_t5_t = document.getElementById('f4_t5_time');
                if (f4_t5_t) {
                    f4_t5_t.value = rtpaTime;
                    syncT5_fromF4();
                }
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

        if (isCaseExcluded()) {
            cohortBadge.innerHTML = '<span style="background: #fee2e2; color: #991b1b; padding: 4px 14px; border-radius: 999px; font-weight: 800; font-size: 13.5px; border: 1.5px solid #dc2626; display: inline-flex; align-items: center; gap: 6px;">⛔ EXCLUDED CASE (ไม่นำเข้า Cohort การศึกษา)</span>';
            cohortFactorsEl.innerHTML = `
                <div style="background: #fff1f2; border: 1px solid #fecdd3; border-radius: 6px; padding: 12px; color: #9f1239; font-size: 13px;">
                    ⚠️ ผู้ป่วยรายนี้ถูกคัดออกจากการศึกษา (Ineligible / Excluded) เนื่องจากไม่ผ่านเกณฑ์การคัดเข้าหรือตรงกับเกณฑ์การคัดออกในส่วนที่ 1 จึงไม่ถูกนำเข้า Cohort การศึกษา
                </div>
            `;
            if (timelineSummary) {
                timelineSummary.innerHTML = '<span style="background: #f1f5f9; color: #64748b; padding: 3px 10px; border-radius: 999px; font-weight: 600; font-size: 12px;">ไม่ได้ประเมิน (Excluded)</span>';
            }
            if (delayBadge) {
                delayBadge.innerHTML = '0 จุด';
                delayBadge.className = 'badge-calc';
            }
            timelineDelaysEl.innerHTML = '<div style="color: #64748b; font-size: 12.5px; padding: 8px 0;">ไม่มีการประเมินความล่าช้าสำหรับเคสที่ถูกคัดออกจากการศึกษา</div>';
            return;
        }

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
        syncT5_bidirectional();
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
        toggleIntubationDetails();
        toggleInotropesDetails();
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
        // Reset inactive conditional pre-transfer sub-fields
        if (data.f1_intubation !== '1') {
            data.f1_ett_no = '';
            data.f1_ett_time = '';
        }
        if (data.f1_inotropes !== '1') {
            data.f1_inotropes_name = '';
            data.f1_inotropes_dose = '';
        }

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
        toggleIntubationDetails();
        toggleInotropesDetails();
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
                alert('⚠️ บันทึกข้อมูลฉบับร่างแล้ว แต่ยังไม่ได้ติ๊กเลือกกลุ่มโรคในเกณฑ์การคัดเข้าข้อ 4\\n(บังคับเลือก 1 กลุ่มโรค: STEMI, Acute Stroke หรือ Severe Trauma)');
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
            toggleIntubationDetails();
            toggleInotropesDetails();

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
                Target_Disease: (c.f1_target_disease === 'ais' || c.f1_inc4_ais) ? 'Acute Stroke' : (c.f1_target_disease === 'stemi' || c.f1_inc4_stemi ? 'STEMI' : (c.f1_target_disease === 'trauma' || c.f1_inc4_trauma ? 'Trauma' : (c.f1_target_disease || ''))),
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
                Target_Disease: (c.f1_target_disease === 'ais' || c.f1_inc4_ais) ? 'Acute Stroke' : (c.f1_target_disease === 'stemi' || c.f1_inc4_stemi ? 'STEMI' : (c.f1_target_disease === 'trauma' || c.f1_inc4_trauma ? 'Trauma' : (c.f1_target_disease || ''))),
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

    // --- JSON IMPORT ENGINE ---
    function handleAdminImportJson(event) {
        const file = event.target.files && event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const parsed = JSON.parse(e.target.result);
                let casesList = [];
                if (Array.isArray(parsed)) {
                    casesList = parsed;
                } else if (parsed && typeof parsed === 'object' && parsed.cases) {
                    casesList = Object.values(parsed.cases);
                } else if (parsed && typeof parsed === 'object' && parsed.studyId) {
                    casesList = [parsed];
                } else {
                    alert('รูปแบบไฟล์ JSON ไม่ถูกต้อง กรุณาใช้ไฟล์ที่ส่งออกจากระบบหรือไฟล์ mock cases');
                    return;
                }

                if (casesList.length === 0) {
                    alert('ไม่พบข้อมูลเคสในไฟล์ JSON');
                    return;
                }

                let index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
                let importedCount = 0;

                casesList.forEach(c => {
                    const sid = c.studyId || c.f1_study_id;
                    if (!sid) return;
                    if (!index.includes(sid)) {
                        index.push(sid);
                    }
                    localStorage.setItem('online_crf_case_' + sid, JSON.stringify(c));
                    importedCount++;
                });

                localStorage.setItem('online_crf_case_index', JSON.stringify(index));

                // If no active case, set first imported case
                if (!localStorage.getItem('online_crf_last_active_id') && casesList[0]) {
                    const firstId = casesList[0].studyId || casesList[0].f1_study_id;
                    if (firstId) localStorage.setItem('online_crf_last_active_id', firstId);
                }

                // Reset file input
                event.target.value = '';

                // Re-render admin dashboard
                if (typeof renderAdminDashboard === 'function') {
                    renderAdminDashboard();
                }

                alert('✓ นำเข้าข้อมูลสำเร็จเรียบร้อยแล้ว จำนวน ' + importedCount + ' เคส');
            } catch (err) {
                console.error('Import JSON Error:', err);
                alert('เกิดข้อผิดพลาดในการอ่านไฟล์ JSON: ' + err.message);
            }
        };
        reader.readAsText(file, 'utf-8');
    }
    if (typeof window !== 'undefined') {
        window.handleAdminImportJson = handleAdminImportJson;
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
                const sex = (data.f1_sex === '1' || data.f1_sex === 'male') ? 'ชาย' : ((data.f1_sex === '2' || data.f1_sex === 'female') ? 'หญิง' : '');
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
        try {
            renderAdminDashboard();
        } catch (e) {
            console.error("Admin Dashboard render error:", e);
        }
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

    // =========================================================================
    // RESEARCH ADMIN DASHBOARD & CLINICAL OBJECTIVES ANALYTICS ENGINE
    // =========================================================================

    // Tab Switching for Admin Dashboard (7 Sub-tabs)
    function switchAdminSubTab(tabName) {
        const tabs = ['overview', 'primary', 'sec1', 'sec2', 'sec3', 'deterioration', 'missing'];
        tabs.forEach(t => {
            const btn = document.getElementById('admin-tab-btn-' + t);
            const pane = document.getElementById('admin-tab-content-' + t);
            if (btn) {
                if (t === tabName) btn.classList.add('active');
                else btn.classList.remove('active');
            }
            if (pane) {
                pane.style.display = (t === tabName) ? 'block' : 'none';
            }
        });
    }

    // Reset Cohort Filters
    function resetAdminFilters() {
        const dis = document.getElementById('admin-filter-disease');
        if (dis) dis.value = '';
        const esi = document.getElementById('admin-filter-esi');
        if (esi) esi.value = '';
        const coh = document.getElementById('admin-filter-cohort');
        if (coh) coh.value = '';
        const search = document.getElementById('admin-search-box');
        if (search) search.value = '';
        renderAdminDashboard();
    }

    // Statistical Helpers
    function calcMean(arr) {
        if (!arr || arr.length === 0) return 0;
        return arr.reduce((a, b) => a + b, 0) / arr.length;
    }

    function calcSD(arr) {
        if (!arr || arr.length <= 1) return 0;
        const m = calcMean(arr);
        const sumSq = arr.reduce((acc, v) => acc + Math.pow(v - m, 2), 0);
        return Math.sqrt(sumSq / (arr.length - 1));
    }

    function calcMedian(arr) {
        if (!arr || arr.length === 0) return 0;
        const sorted = [...arr].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        return sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
    }

    function calcIQRStr(arr) {
        if (!arr || arr.length === 0) return '-';
        const sorted = [...arr].sort((a, b) => a - b);
        const q1 = sorted[Math.floor(sorted.length * 0.25)];
        const q3 = sorted[Math.floor(sorted.length * 0.75)];
        return `[${q1.toFixed(0)} - ${q3.toFixed(0)}]`;
    }

    // Case Exposure Checker for Cohort Classification
    function checkCaseExposure(data) {
        const isTrauma = Boolean(data.f1_target_disease === 'trauma' || data.f1_inc4_trauma || data.f1_cond_trauma);
        const totalMin = parseFloat(data.f2_t_total_min || data.f2_eq1_total_transfer);
        const totalLimit = isTrauma ? 156 : 141;
        const isTotalDelay = (!isNaN(totalMin) && totalMin > totalLimit) || data.f2_total_delay;

        const isOffHour = data.f2_ferry_operate === '1' || data.f3_ferry_shift === '1';
        const isRoughSea = data.f3_sea_state === '2' || (parseFloat(data.f3_wave_height) > 2.0);
        const isLowTide = data.f3_tide_extreme === '1' || data.f3_sandbar_risk === '1' || (parseFloat(data.f3_tide_height) < 1.0);
        const isTorrentialRain = data.f3_precipitation === '1' && (data.f3_torrential_rain === '1' || parseFloat(data.f3_rainfall_mm) >= 10.0);
        const isMonsoonSwell = (data.f3_season === '0' && isRoughSea);
        const isPierCongest = data.f2_pier_congestion === '1';

        return isTotalDelay || isOffHour || isRoughSea || isLowTide || isTorrentialRain || isMonsoonSwell || isPierCongest;
    }

    // --- Data Quality & Completeness Audit Variables Schema ---
    function isCaseStemi(data) {
        if (!data) return false;
        return Boolean(data.f1_target_disease === 'stemi' || data.f1_inc4_stemi || data.f1_cond_stemi);
    }
    function isCaseStroke(data) {
        if (!data) return false;
        return Boolean(data.f1_target_disease === 'ais' || data.f1_inc4_ais || data.f1_cond_stroke);
    }
    function isCaseTrauma(data) {
        if (!data) return false;
        return Boolean(data.f1_target_disease === 'trauma' || data.f1_inc4_trauma || data.f1_cond_trauma);
    }

    function isFieldFilled(data, key) {
        if (!data) return false;
        if (key === 'f1_gcs_total') {
            if (data.f1_gcs_total !== undefined && data.f1_gcs_total !== null && String(data.f1_gcs_total).trim() !== '') return true;
            if (data.f1_gcs_e && data.f1_gcs_v && data.f1_gcs_m) return true;
            return false;
        }
        if (key === 'f4_gcs_total') {
            if (data.f4_gcs_total !== undefined && data.f4_gcs_total !== null && String(data.f4_gcs_total).trim() !== '') return true;
            if (data.f4_gcs_e && data.f4_gcs_v && data.f4_gcs_m) return true;
            return false;
        }
        const val = data[key];
        return (val !== undefined && val !== null && String(val).trim() !== '');
    }

const CRF_AUDIT_FIELDS = [
        // ==========================================
        // Form 1: ข้อมูลแรกรับและคัดกรอง ณ รพ.เกาะลันตา
        // ==========================================
        // ข้อมูลทั่วไปและผู้สกัด
        { key: 'f1_refer_id', label: 'เลขที่ใบส่งต่อ (Refer_ID)', form: 1, formName: 'Form 1', category: 'ข้อมูลทั่วไปและผู้สกัด', type: 'text', placeholder: 'ระบุเลขที่ใบส่งต่อ' },
        { key: 'f1_hn', label: 'เลขประจำตัวผู้ป่วย (HN เกาะลันตา)', form: 1, formName: 'Form 1', category: 'ข้อมูลทั่วไปและผู้สกัด', type: 'text', placeholder: 'HN รพ.เกาะลันตา' },
        { key: 'f1_vn', label: 'เลข VN เกาะลันตา', form: 1, formName: 'Form 1', category: 'ข้อมูลทั่วไปและผู้สกัด', type: 'text', placeholder: 'VN รพ.เกาะลันตา' },
        { key: 'f1_abs_date', label: 'วันที่สกัดข้อมูล (Abstract Date)', form: 1, formName: 'Form 1', category: 'ข้อมูลทั่วไปและผู้สกัด', type: 'date' },
        { key: 'f1_abstractor', label: 'ชื่อผู้สกัดข้อมูล (Abstractor)', form: 1, formName: 'Form 1', category: 'ข้อมูลทั่วไปและผู้สกัด', type: 'text', placeholder: 'ชื่อผู้สกัดข้อมูล' },

        // เกณฑ์การคัดกรองวิจัย
        { key: 'f1_target_disease', label: 'กลุ่มโรคเป้าหมาย (Target Disease)', form: 1, formName: 'Form 1', category: 'เกณฑ์การคัดกรองวิจัย', type: 'select', options: [
            { value: 'stemi', label: '1. STEMI / Acute Coronary Syndrome (ACS)' },
            { value: 'ais', label: '2. Acute Stroke' },
            { value: 'trauma', label: '3. Severe Trauma (อุบัติเหตุบาดเจ็บรุนแรง)' }
        ]},
        { key: 'f1_inc1', label: 'เกณฑ์คัดเข้า: อายุ ≥ 18 ปี', form: 1, formName: 'Form 1', category: 'เกณฑ์การคัดกรองวิจัย', type: 'select', options: [{ value: 'yes', label: 'ใช่' }, { value: 'no', label: 'ไม่ใช่' }] },
        { key: 'f1_inc2', label: 'เกณฑ์คัดเข้า: รับไว้รักษา ณ ER เกาะลันตา', form: 1, formName: 'Form 1', category: 'เกณฑ์การคัดกรองวิจัย', type: 'select', options: [{ value: 'yes', label: 'ใช่' }, { value: 'no', label: 'ไม่ใช่' }] },
        { key: 'f1_inc3', label: 'เกณฑ์คัดเข้า: ส่งต่อเร่งด่วนสู่ รพ.กระบี่', form: 1, formName: 'Form 1', category: 'เกณฑ์การคัดกรองวิจัย', type: 'select', options: [{ value: 'yes', label: 'ใช่' }, { value: 'no', label: 'ไม่ใช่' }] },
        { key: 'f1_inc4', label: 'เกณฑ์คัดเข้า: เข้าเกณฑ์วินิจฉัยกลุ่มโรคเป้าหมาย', form: 1, formName: 'Form 1', category: 'เกณฑ์การคัดกรองวิจัย', type: 'select', options: [{ value: 'yes', label: 'ใช่' }, { value: 'no', label: 'ไม่ใช่' }] },
        { key: 'f1_exc1', label: 'เกณฑ์คัดออก: ผู้ป่วย/ญาติปฏิเสธการส่งต่อ', form: 1, formName: 'Form 1', category: 'เกณฑ์การคัดกรองวิจัย', type: 'select', options: [{ value: 'no', label: 'ไม่ใช่' }, { value: 'yes', label: 'ใช่ (คัดออก)' }] },
        { key: 'f1_exc2', label: 'เกณฑ์คัดออก: ส่งต่อไปยัง รพ.เอกชนหรือนอกระบบ', form: 1, formName: 'Form 1', category: 'เกณฑ์การคัดกรองวิจัย', type: 'select', options: [{ value: 'no', label: 'ไม่ใช่' }, { value: 'yes', label: 'ใช่ (คัดออก)' }] },
        { key: 'f1_exc3', label: 'เกณฑ์คัดออก: เวชระเบียนสูญหายเกิน 50%', form: 1, formName: 'Form 1', category: 'เกณฑ์การคัดกรองวิจัย', type: 'select', options: [{ value: 'no', label: 'ไม่ใช่' }, { value: 'yes', label: 'ใช่ (คัดออก)' }] },
        { key: 'f1_exc4', label: 'เกณฑ์คัดออก: เสียชีวิตก่อนถึงห้องฉุกเฉิน (DOA)', form: 1, formName: 'Form 1', category: 'เกณฑ์การคัดกรองวิจัย', type: 'select', options: [{ value: 'no', label: 'ไม่ใช่' }, { value: 'yes', label: 'ใช่ (คัดออก)' }] },

        // ประชากรศาสตร์
        { key: 'f1_age', label: 'อายุ (Age)', form: 1, formName: 'Form 1', category: 'ประชากรศาสตร์', type: 'number', unit: 'ปี', min: 0, max: 120 },
        { key: 'f1_sex', label: 'เพศกำเนิด (Sex)', form: 1, formName: 'Form 1', category: 'ประชากรศาสตร์', type: 'select', options: [{ value: 'male', label: 'ชาย (Male)' }, { value: 'female', label: 'หญิง (Female)' }] },
        { key: 'f1_nationality', label: 'สัญชาติ (Nationality)', form: 1, formName: 'Form 1', category: 'ประชากรศาสตร์', type: 'text', placeholder: 'เช่น ไทย, อังกฤษ, สวีเดน' },
        { key: 'f1_residency', label: 'สถานะประชากร (Residency)', form: 1, formName: 'Form 1', category: 'ประชากรศาสตร์', type: 'select', options: [
            { value: '1', label: '1 = ชาวเกาะในพื้นที่ (Islander)' },
            { value: '2', label: '2 = นักท่องเที่ยวไทย (Thai tourist)' },
            { value: '3', label: '3 = นักท่องเที่ยวต่างชาติ (Foreigner)' },
            { value: '4', label: '4 = แรงงานข้ามชาติ (Migrant worker)' }
        ]},
        { key: 'f1_premrs', label: 'ระดับความพิการเดิม (Pre-morbid mRS)', form: 1, formName: 'Form 1', category: 'ประชากรศาสตร์', type: 'select', options: [
            { value: '0', label: '0 = ปกติ ไม่มีอาการ' },
            { value: '1', label: '1 = ไม่มีทุพพลภาพ ทำงานได้ปกติ' },
            { value: '2', label: '2 = เล็กน้อย ดูแลตนเองได้' },
            { value: '3', label: '3 = ปานกลาง เดินได้เอง' },
            { value: '4', label: '4 = มาก ช่วยตนเองไม่ได้' },
            { value: '5', label: '5 = นอนติดเตียง ต้องการดูแลตลอดเวลา' }
        ]},

        // ภาวะโรคร่วมจำเพาะ (CCI Subtypes)
        { key: 'f1_cci_dm_type', label: 'ชนิดโรคเบาหวาน (DM Subtype)', form: 1, formName: 'Form 1', category: 'ประชากรศาสตร์และโรคร่วม', type: 'select', condition: d => Boolean(d.f1_cci_dm_chk), options: [
            { value: '1', label: 'ไม่มีภาวะแทรกซ้อน (+1)' },
            { value: '2', label: 'มีภาวะแทรกซ้อน (+2)' }
        ]},
        { key: 'f1_cci_liver_type', label: 'ความรุนแรงโรคตับ (Liver Disease Severity)', form: 1, formName: 'Form 1', category: 'ประชากรศาสตร์และโรคร่วม', type: 'select', condition: d => Boolean(d.f1_cci_liver_chk), options: [
            { value: '1', label: 'ไม่รุนแรง (+1)' },
            { value: '3', label: 'ปานกลางถึงรุนแรงมาก (+3)' }
        ]},
        { key: 'f1_cci_tumor_type', label: 'ระยะมะเร็งก้อน (Solid Tumor Staging)', form: 1, formName: 'Form 1', category: 'ประชากรศาสตร์และโรคร่วม', type: 'select', condition: d => Boolean(d.f1_cci_tumor_chk), options: [
            { value: '2', label: 'ไม่แพร่กระจาย (+2)' },
            { value: '6', label: 'ระยะแพร่กระจาย (+6)' }
        ]},


        // แรกรับ ER เกาะลันตา
        { key: 'f1_onset_date', label: 'วันที่เริ่มมีอาการ (Onset Date)', form: 1, formName: 'Form 1', category: 'แรกรับ ER เกาะลันตา', type: 'date' },
        { key: 'f1_onset_time', label: 'เวลาเริ่มมีอาการ (Onset Time)', form: 1, formName: 'Form 1', category: 'แรกรับ ER เกาะลันตา', type: 'time' },
        { key: 'f1_t0_date', label: 'วันที่ถึง ER เกาะลันตา (T0 Date)', form: 1, formName: 'Form 1', category: 'แรกรับ ER เกาะลันตา', type: 'date' },
        { key: 'f1_t0_time', label: 'เวลาถึง ER เกาะลันตา (T0 Time)', form: 1, formName: 'Form 1', category: 'แรกรับ ER เกาะลันตา', type: 'time' },
        { key: 'f1_arrival_mode', label: 'รูปแบบการมา ER (Arrival Mode)', form: 1, formName: 'Form 1', category: 'แรกรับ ER เกาะลันตา', type: 'select', options: [
            { value: '1', label: '1 = รถพยาบาล 1669 / กู้ภัย (EMS)' },
            { value: '2', label: '2 = มาเอง / ญาติพามา (Walk-in)' }
        ]},
        { key: 'f1_esi', label: 'ระดับความเร่งด่วน Triage ESI', form: 1, formName: 'Form 1', category: 'แรกรับ ER เกาะลันตา', type: 'select', options: [
            { value: '1', label: 'ESI 1 (Resuscitation)' },
            { value: '2', label: 'ESI 2 (Emergent)' }
        ]},
        { key: 'f1_shift', label: 'เวรแรกรับ ER (ED Shift)', form: 1, formName: 'Form 1', category: 'แรกรับ ER เกาะลันตา', type: 'select', options: [
            { value: 'morning', label: 'เวรเช้า (08:00–16:00 น.)' },
            { value: 'afternoon', label: 'เวรบ่าย (16:00–24:00 น.)' },
            { value: 'night', label: 'เวรดึก (00:00–08:00 น.)' }
        ]},

        // สัญญาณชีพแรกรับ
        { key: 'f1_sbp', label: 'SBP แรกรับเกาะลันตา', form: 1, formName: 'Form 1', category: 'สัญญาณชีพแรกรับ', type: 'number', unit: 'mmHg' },
        { key: 'f1_dbp', label: 'DBP แรกรับเกาะลันตา', form: 1, formName: 'Form 1', category: 'สัญญาณชีพแรกรับ', type: 'number', unit: 'mmHg' },
        { key: 'f1_hr', label: 'ชีพจรแรกรับ (Heart Rate)', form: 1, formName: 'Form 1', category: 'สัญญาณชีพแรกรับ', type: 'number', unit: 'bpm' },
        { key: 'f1_rr', label: 'อัตราหายใจแรกรับ (Resp Rate)', form: 1, formName: 'Form 1', category: 'สัญญาณชีพแรกรับ', type: 'number', unit: '/min' },
        { key: 'f1_spo2', label: 'ออกซิเจนในเลือด (SpO2)', form: 1, formName: 'Form 1', category: 'สัญญาณชีพแรกรับ', type: 'number', unit: '%' },
        { key: 'f1_o2support', label: 'การใช้ออกซิเจนแรกรับ (O2 Support)', form: 1, formName: 'Form 1', category: 'สัญญาณชีพแรกรับ', type: 'select', options: [
            { value: 'ra', label: 'Room Air (หายใจอากาศปกติ)' },
            { value: 'o2', label: 'O2 Support (ได้รับออกซิเจนเสริม)' }
        ]},
        { key: 'f1_bt', label: 'อุณหภูมิกายแรกรับ (Body Temp)', form: 1, formName: 'Form 1', category: 'สัญญาณชีพแรกรับ', type: 'number', unit: '°C', step: '0.1' },
        { key: 'f1_gcs_total', label: 'คะแนนความรู้สึกตัว (GCS Total)', form: 1, formName: 'Form 1', category: 'สัญญาณชีพแรกรับ', type: 'number', unit: 'คะแนน', min: 3, max: 15 },

        // ความรุนแรงจำเพาะโรค
        { key: 'f1_killip', label: 'ระดับความรุนแรง Killip (STEMI)', form: 1, formName: 'Form 1', category: 'ความรุนแรงจำเพาะโรค', type: 'select', condition: isCaseStemi, options: [
            { value: '1', label: 'Killip I (ไม่มีหัวใจล้มเหลว)' },
            { value: '2', label: 'Killip II (มี Rales / S3)' },
            { value: '3', label: 'Killip III (Pulmonary edema)' },
            { value: '4', label: 'Killip IV (Cardiogenic shock)' }
        ]},
        { key: 'f1_stroke_gcs', label: 'ระดับความรู้สึกตัว Stroke GCS', form: 1, formName: 'Form 1', category: 'ความรุนแรงจำเพาะโรค', type: 'select', condition: isCaseStroke, options: [
            { value: 'severe', label: 'GCS 3–8: Severe Coma (โคม่ารุนแรง)' },
            { value: 'moderate', label: 'GCS 9–12: Moderate (ความรู้สึกตัวลดลงปานกลาง)' },
            { value: 'mild', label: 'GCS 13–15: Mild (สับสนเล็กน้อยหรือรู้สึกตัวดี)' }
        ]},
        { key: 'f1_trauma_acuity', label: 'ระดับความรุนแรงบาดเจ็บ Trauma Acuity', form: 1, formName: 'Form 1', category: 'ความรุนแรงจำเพาะโรค', type: 'select', condition: isCaseTrauma, options: [
            { value: 'critical', label: 'RTS ≤ 6: Critical (วิกฤต)' },
            { value: 'moderate', label: 'RTS > 6: Moderate (ปานกลาง)' }
        ]},

        // การช่วยกู้ชีพ ณ เกาะลันตา
        { key: 'f1_intubation', label: 'การใส่ท่อช่วยหายใจ ณ รพ.เกาะลันตา', form: 1, formName: 'Form 1', category: 'การช่วยกู้ชีพ ณ เกาะลันตา', type: 'select', options: [
            { value: '0', label: '0 = ไม่ได้ใส่' },
            { value: '1', label: '1 = ใส่ท่อช่วยหายใจตั้งแต่ รพ.เกาะลันตา' }
        ]},
        { key: 'f1_ett_no', label: 'ขนาดท่อช่วยหายใจ (ETT No.)', form: 1, formName: 'Form 1', category: 'การช่วยกู้ชีพ ณ เกาะลันตา', type: 'text', condition: d => d.f1_intubation === '1', placeholder: 'เช่น 7.0, 7.5, 8.0' },
        { key: 'f1_ett_time', label: 'เวลาใส่ท่อช่วยหายใจ ณ เกาะลันตา', form: 1, formName: 'Form 1', category: 'การช่วยกู้ชีพ ณ เกาะลันตา', type: 'time', condition: d => d.f1_intubation === '1' },
        { key: 'f1_inotropes', label: 'การให้ยากระตุ้นความดัน ณ เกาะลันตา', form: 1, formName: 'Form 1', category: 'การช่วยกู้ชีพ ณ เกาะลันตา', type: 'select', options: [
            { value: '0', label: '0 = ไม่ได้รับ' },
            { value: '1', label: '1 = ได้รับยากระตุ้นความดัน' }
        ]},
        { key: 'f1_inotropes_name', label: 'ชื่อยากระตุ้นความดัน ณ เกาะลันตา', form: 1, formName: 'Form 1', category: 'การช่วยกู้ชีพ ณ เกาะลันตา', type: 'text', condition: d => d.f1_inotropes === '1', placeholder: 'เช่น Norepinephrine, Dopamine' },
        { key: 'f1_inotropes_dose', label: 'ขนาดยากระตุ้นความดัน ณ เกาะลันตา', form: 1, formName: 'Form 1', category: 'การช่วยกู้ชีพ ณ เกาะลันตา', type: 'text', condition: d => d.f1_inotropes === '1', placeholder: 'เช่น 0.1 mcg/kg/min' },

        // ส่งต่อออกจากเกาะ (DIDO)
        { key: 'f1_t1_date', label: 'วันที่ออกจาก ER เกาะลันตา (T1 Date)', form: 1, formName: 'Form 1', category: 'ส่งต่อออกจากเกาะ (DIDO)', type: 'date' },
        { key: 'f1_t1_time', label: 'เวลาออกจาก ER เกาะลันตา (T1 Time)', form: 1, formName: 'Form 1', category: 'ส่งต่อออกจากเกาะ (DIDO)', type: 'time' },
        { key: 'f1_dido_eval', label: 'การประเมินกรอบเวลา DIDO เกาะลันตา', form: 1, formName: 'Form 1', category: 'ส่งต่อออกจากเกาะ (DIDO)', type: 'select', options: [
            { value: 'ontime', label: 'ทันเกณฑ์ (≤ 45m / ≤ 60m)' },
            { value: 'delay', label: 'ล่าช้า (DIDO Delay Breach)' }
        ]},

        // ==========================================
        // Form 2: ไทม์ไลน์และเหตุการณ์ระหว่างส่งต่อทางทะเลและบก
        // ==========================================
        // ทีมส่งต่อ
        { key: 'f2_amb_plate', label: 'ทะเบียนรถพยาบาล (Ambulance Plate)', form: 2, formName: 'Form 2', category: 'ทีมส่งต่อ', type: 'text', placeholder: 'เช่น กข-1234 กระบี่' },
        { key: 'f2_escort_rn', label: 'ชื่อพยาบาลนำส่ง (Escort RN)', form: 2, formName: 'Form 2', category: 'ทีมส่งต่อ', type: 'text', placeholder: 'ชื่อ-สกุล พยาบาล' },
        { key: 'f2_driver', label: 'พนักงานขับรถพยาบาล', form: 2, formName: 'Form 2', category: 'ทีมส่งต่อ', type: 'text', placeholder: 'ชื่อ-สกุล พนักงานขับรถ' },

        // หมุดเวลาการนำส่ง
        { key: 'f2_t2_date', label: 'วันที่ถึงท่าเรือคลองหมาก (T2 Date)', form: 2, formName: 'Form 2', category: 'หมุดเวลาการนำส่ง', type: 'date' },
        { key: 'f2_t2_time', label: 'เวลาถึงท่าเรือคลองหมาก (T2 Time)', form: 2, formName: 'Form 2', category: 'หมุดเวลาการนำส่ง', type: 'time' },
        { key: 'f2_t3_embark_date', label: 'วันที่รถขึ้นแพขนานยนต์ (T3 Embark Date)', form: 2, formName: 'Form 2', category: 'หมุดเวลาการนำส่ง', type: 'date' },
        { key: 'f2_t3_embark_time', label: 'เวลารถขึ้นแพขนานยนต์ (T3 Embark Time)', form: 2, formName: 'Form 2', category: 'หมุดเวลาการนำส่ง', type: 'time' },
        { key: 'f2_t3_disembark_date', label: 'วันที่รถลงแพถึงท่าหัวหิน (T3 Disembark Date)', form: 2, formName: 'Form 2', category: 'หมุดเวลาการนำส่ง', type: 'date' },
        { key: 'f2_t3_disembark_time', label: 'เวลารถลงแพถึงท่าหัวหิน (T3 Disembark Time)', form: 2, formName: 'Form 2', category: 'หมุดเวลาการนำส่ง', type: 'time' },
        { key: 'f2_t4_date', label: 'วันที่ถึง ER รพ.กระบี่ (T4 Date)', form: 2, formName: 'Form 2', category: 'หมุดเวลาการนำส่ง', type: 'date' },
        { key: 'f2_t4_time', label: 'เวลาถึง ER รพ.กระบี่ (T4 Time)', form: 2, formName: 'Form 2', category: 'หมุดเวลาการนำส่ง', type: 'time' },
        { key: 'f2_t5_date', label: 'วันที่เริ่ม Definitive Care (T5 Date)', form: 2, formName: 'Form 2', category: 'หมุดเวลาการนำส่ง', type: 'date' },
        { key: 'f2_t5_time', label: 'เวลาเริ่ม Definitive Care (T5 Time)', form: 2, formName: 'Form 2', category: 'หมุดเวลาการนำส่ง', type: 'time' },

        // การประเมินช่วงเวลาส่งต่อ
        { key: 'f2_eval_dido', label: 'ผลประเมิน T0-1 Island DIDO', form: 2, formName: 'Form 2', category: 'การประเมินช่วงเวลาส่งต่อ', type: 'select', options: [
            { value: 'ontime', label: 'ทันเกณฑ์ (≤ 45m / ≤ 60m)' },
            { value: 'delay', label: 'ล่าช้า (> 45m / > 60m)' }
        ]},
        { key: 'f2_eval_road', label: 'ผลประเมิน T2 Island Road', form: 2, formName: 'Form 2', category: 'การประเมินช่วงเวลาส่งต่อ', type: 'select', options: [
            { value: 'ontime', label: 'ทันเกณฑ์ (≤ 12 นาที)' },
            { value: 'delay', label: 'ล่าช้า (> 12 นาที)' }
        ]},
        { key: 'f2_eval_water', label: 'ผลประเมิน T3 Water Crossing', form: 2, formName: 'Form 2', category: 'การประเมินช่วงเวลาส่งต่อ', type: 'select', options: [
            { value: 'ontime', label: 'ทันเกณฑ์ (≤ 24 นาที)' },
            { value: 'delay', label: 'ล่าช้า (> 24 นาที)' }
        ]},
        { key: 'f2_eval_wait', label: 'ผลประเมินเวลารอขึ้นแพขนานยนต์', form: 2, formName: 'Form 2', category: 'การประเมินช่วงเวลาส่งต่อ', type: 'select', options: [
            { value: 'ontime', label: 'ปกติ (≤ 5 นาที)' },
            { value: 'delay', label: 'รอคิวนาน (> 5 นาที)' }
        ]},
        { key: 'f2_eval_hwy', label: 'ผลประเมิน T4 Mainland Highway', form: 2, formName: 'Form 2', category: 'การประเมินช่วงเวลาส่งต่อ', type: 'select', options: [
            { value: 'ontime', label: 'ทันเกณฑ์ (≤ 60 นาที)' },
            { value: 'delay', label: 'ล่าช้า (> 60 นาที)' }
        ]},
        { key: 'f2_eval_total', label: 'ผลประเมิน T_Total System Time รวม', form: 2, formName: 'Form 2', category: 'การประเมินช่วงเวลาส่งต่อ', type: 'select', options: [
            { value: 'ontime', label: 'ทันเกณฑ์ (≤ 141m / ≤ 156m)' },
            { value: 'delay', label: 'ล่าช้า (> 141m / > 156m)' }
        ]},
        { key: 'f2_eval_t5', label: 'ผลประเมิน T5 Definitive Management', form: 2, formName: 'Form 2', category: 'การประเมินช่วงเวลาส่งต่อ', type: 'select', options: [
            { value: 'ontime', label: 'ทันเกณฑ์ (≤ 156m / ≤ 180m)' },
            { value: 'delay', label: 'ล่าช้า (> 156m / > 180m)' }
        ]},

        // บริบทแพขนานยนต์
        { key: 'f2_ferry_operate', label: 'ช่วงเวลาเดินแพขนานยนต์ (Ferry Period)', form: 2, formName: 'Form 2', category: 'บริบทแพขนานยนต์', type: 'select', options: [
            { value: '0', label: '0 = Scheduled Daytime (05:00–24:00 น.) เดินแพปกติ' },
            { value: '1', label: '1 = Standby Off-Hour (24:00–05:00 น.) โทรตามแพพิเศษ' }
        ]},
        { key: 'f2_pier_congestion', label: 'ภาวะคิวแพติดสะสม (Pier Congestion)', form: 2, formName: 'Form 2', category: 'บริบทแพขนานยนต์', type: 'select', options: [
            { value: '0', label: '0 = ไม่มีคิวสะสม รถพยาบาลลงแพได้ทันที' },
            { value: '1', label: '1 = มีคิวรถสะสมหน้าท่าข้ามแพ' }
        ]},
        { key: 'f2_ferry_count', label: 'จำนวนแพขนานยนต์ที่พร้อมให้บริการ', form: 2, formName: 'Form 2', category: 'บริบทแพขนานยนต์', type: 'select', options: [
            { value: '1', label: '1 ลำ' },
            { value: '2', label: '2 ลำ' },
            { value: '3', label: '3 ลำ' }
        ]},

        // สัญญาณชีพระหว่างทาง (จุดสังเกตการณ์ 1 - ทางหลวงบนเกาะ)
        { key: 'f2_mon1_time', label: 'เวลาจุดที่ 1 ทางหลวงบนเกาะ', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 1)', type: 'time' },
        { key: 'f2_mon1_sbp', label: 'SBP จุดที่ 1 ทางหลวงบนเกาะ', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 1)', type: 'number', unit: 'mmHg' },
        { key: 'f2_mon1_dbp', label: 'DBP จุดที่ 1 ทางหลวงบนเกาะ', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 1)', type: 'number', unit: 'mmHg' },
        { key: 'f2_mon1_hr', label: 'ชีพจร จุดที่ 1 ทางหลวงบนเกาะ', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 1)', type: 'number', unit: 'bpm' },
        { key: 'f2_mon1_rr', label: 'อัตราหายใจ จุดที่ 1 ทางหลวงบนเกาะ', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 1)', type: 'number', unit: '/min' },
        { key: 'f2_mon1_spo2', label: 'SpO2 จุดที่ 1 ทางหลวงบนเกาะ', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 1)', type: 'number', unit: '%' },
        { key: 'f2_mon1_gcs', label: 'GCS จุดที่ 1 ทางหลวงบนเกาะ', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 1)', type: 'number', unit: 'คะแนน', min: 3, max: 15 },

        // สัญญาณชีพระหว่างทาง (จุดสังเกตการณ์ 2 - บนแพขนานยนต์)
        { key: 'f2_mon2_time', label: 'เวลาจุดที่ 2 บนแพขนานยนต์', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 2)', type: 'time' },
        { key: 'f2_mon2_sbp', label: 'SBP จุดที่ 2 บนแพขนานยนต์', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 2)', type: 'number', unit: 'mmHg' },
        { key: 'f2_mon2_dbp', label: 'DBP จุดที่ 2 บนแพขนานยนต์', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 2)', type: 'number', unit: 'mmHg' },
        { key: 'f2_mon2_hr', label: 'ชีพจร จุดที่ 2 บนแพขนานยนต์', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 2)', type: 'number', unit: 'bpm' },
        { key: 'f2_mon2_rr', label: 'อัตราหายใจ จุดที่ 2 บนแพขนานยนต์', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 2)', type: 'number', unit: '/min' },
        { key: 'f2_mon2_spo2', label: 'SpO2 จุดที่ 2 บนแพขนานยนต์', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 2)', type: 'number', unit: '%' },
        { key: 'f2_mon2_gcs', label: 'GCS จุดที่ 2 บนแพขนานยนต์', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 2)', type: 'number', unit: 'คะแนน', min: 3, max: 15 },

        // สัญญาณชีพระหว่างทาง (จุดสังเกตการณ์ 3 - ทางหลวงแผ่นดิน กม.35)
        { key: 'f2_mon3_time', label: 'เวลาจุดที่ 3 ทางหลวงแผ่นดิน', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 3)', type: 'time' },
        { key: 'f2_mon3_sbp', label: 'SBP จุดที่ 3 ทางหลวงแผ่นดิน', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 3)', type: 'number', unit: 'mmHg' },
        { key: 'f2_mon3_dbp', label: 'DBP จุดที่ 3 ทางหลวงแผ่นดิน', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 3)', type: 'number', unit: 'mmHg' },
        { key: 'f2_mon3_hr', label: 'ชีพจร จุดที่ 3 ทางหลวงแผ่นดิน', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 3)', type: 'number', unit: 'bpm' },
        { key: 'f2_mon3_rr', label: 'อัตราหายใจ จุดที่ 3 ทางหลวงแผ่นดิน', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 3)', type: 'number', unit: '/min' },
        { key: 'f2_mon3_spo2', label: 'SpO2 จุดที่ 3 ทางหลวงแผ่นดิน', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 3)', type: 'number', unit: '%' },
        { key: 'f2_mon3_gcs', label: 'GCS จุดที่ 3 ทางหลวงแผ่นดิน', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 3)', type: 'number', unit: 'คะแนน', min: 3, max: 15 },

        // สัญญาณชีพระหว่างทาง (จุดสังเกตการณ์ 4 - หน้า ER รพ.กระบี่)
        { key: 'f2_mon4_time', label: 'เวลาจุดที่ 4 หน้า ER รพ.กระบี่', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 4)', type: 'time' },
        { key: 'f2_mon4_sbp', label: 'SBP จุดที่ 4 หน้า ER รพ.กระบี่', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 4)', type: 'number', unit: 'mmHg' },
        { key: 'f2_mon4_dbp', label: 'DBP จุดที่ 4 หน้า ER รพ.กระบี่', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 4)', type: 'number', unit: 'mmHg' },
        { key: 'f2_mon4_hr', label: 'ชีพจร จุดที่ 4 หน้า ER รพ.กระบี่', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 4)', type: 'number', unit: 'bpm' },
        { key: 'f2_mon4_rr', label: 'อัตราหายใจ จุดที่ 4 หน้า ER รพ.กระบี่', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 4)', type: 'number', unit: '/min' },
        { key: 'f2_mon4_spo2', label: 'SpO2 จุดที่ 4 หน้า ER รพ.กระบี่', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 4)', type: 'number', unit: '%' },
        { key: 'f2_mon4_gcs', label: 'GCS จุดที่ 4 หน้า ER รพ.กระบี่', form: 2, formName: 'Form 2', category: 'สัญญาณชีพระหว่างทาง (จุดที่ 4)', type: 'number', unit: 'คะแนน', min: 3, max: 15 },

        // เหตุการณ์ไม่พึงประสงค์ (AE)
        { key: 'f2_ae_cpr', label: 'มี CPR ระหว่างนำส่ง', form: 2, formName: 'Form 2', category: 'เหตุการณ์ไม่พึงประสงค์ (AE)', type: 'select', options: [
            { value: '0', label: '0 = ไม่มีภาวะหัวใจหยุดเต้น' },
            { value: '1', label: '1 = มีการทำ CPR ระหว่างทาง' }
        ]},
        { key: 'f2_cpr_duration', label: 'ระยะเวลาทำ CPR รวม (นาที)', form: 2, formName: 'Form 2', category: 'เหตุการณ์ไม่พึงประสงค์ (AE)', type: 'number', unit: 'นาที', condition: d => d.f2_ae_cpr === '1' },
        { key: 'f2_cpr_outcome', label: 'ผลลัพธ์การทำ CPR', form: 2, formName: 'Form 2', category: 'เหตุการณ์ไม่พึงประสงค์ (AE)', type: 'select', condition: d => d.f2_ae_cpr === '1', options: [
            { value: 'rosc', label: 'ROSC ก่อนถึง ER' },
            { value: 'ongoing', label: 'ทำ CPR ต่อเนื่องจนถึง ER' }
        ]},
        { key: 'f2_ae_intub', label: 'มีใส่ท่อช่วยหายใจระหว่างทาง', form: 2, formName: 'Form 2', category: 'เหตุการณ์ไม่พึงประสงค์ (AE)', type: 'select', options: [
            { value: '0', label: '0 = ไม่ได้ใส่ระหว่างทาง' },
            { value: '1', label: '1 = มีการใส่ท่อช่วยหายใจฉุกเฉิน' }
        ]},
        { key: 'f2_ae_inotropes', label: 'เริ่ม/ปรับยากระตุ้นความดันระหว่างทาง', form: 2, formName: 'Form 2', category: 'เหตุการณ์ไม่พึงประสงค์ (AE)', type: 'select', options: [
            { value: '0', label: '0 = ขนาดยาคงที่ / ไม่ต้องเริ่มยาใหม่' },
            { value: '1', label: '1 = เริ่มยาใหม่ หรือปรับเพิ่มขนาดยา ≥ 50%' }
        ]},
        { key: 'f2_ae_dislodge', label: 'ท่อช่วยหายใจเลื่อนหลุดระหว่างทาง (ETT Dislodgement)', form: 2, formName: 'Form 2', category: 'เหตุการณ์ไม่พึงประสงค์ (AE)', type: 'select', options: [
            { value: '0', label: '0 = ไม่มี' },
            { value: '1', label: '1 = เกิดท่อช่วยหายใจเลื่อนหลุด' }
        ]},
        { key: 'f2_ae_death', label: 'เสียชีวิตระหว่างนำส่ง (Transit Death)', form: 2, formName: 'Form 2', category: 'เหตุการณ์ไม่พึงประสงค์ (AE)', type: 'select', options: [
            { value: '0', label: '0 = รอดชีวิตจนถึง ER' },
            { value: '1', label: '1 = เสียชีวิตระหว่างนำส่ง' }
        ]},
        { key: 'f2_composite_ae', label: 'สรุปภาวะทรุดหนักระหว่างทางรวม', form: 2, formName: 'Form 2', category: 'เหตุการณ์ไม่พึงประสงค์ (AE)', type: 'select', options: [
            { value: '0', label: '0 = สัญญาณชีพคงที่ตลอดการเดินทาง (Stable)' },
            { value: '1', label: '1 = เกิดภาวะทรุดหนักวิกฤตระหว่างทาง (Critical AE)' }
        ]},

        // ==========================================
        // Form 3: สภาพแวดล้อม อุทกศาสตร์ทางทะเล และอุตุนิยมวิทยา
        // ==========================================
        // วันเวลาข้ามฟาก T3
        { key: 'f3_t3_date', label: 'วันที่ข้ามฟาก T3 (Form 3)', form: 3, formName: 'Form 3', category: 'วันเวลาข้ามฟาก T3', type: 'date' },
        { key: 'f3_t3_time', label: 'เวลาข้ามฟาก T3 (Form 3)', form: 3, formName: 'Form 3', category: 'วันเวลาข้ามฟาก T3', type: 'time' },

        // อุทกศาสตร์ทางทะเล
        { key: 'f3_tide_height', label: 'ระดับความสูงน้ำทะเล ณ เวลา T3', form: 3, formName: 'Form 3', category: 'อุทกศาสตร์ทางทะเล', type: 'number', unit: 'เมตร', step: '0.01' },
        { key: 'f3_tide_phase', label: 'ช่วงเวลาน้ำขึ้น-น้ำลง (Tide Phase)', form: 3, formName: 'Form 3', category: 'อุทกศาสตร์ทางทะเล', type: 'select', options: [
            { value: '1', label: '1 = น้ำขึ้น (High / Flood tide)' },
            { value: '2', label: '2 = น้ำลง (Low / Ebb tide)' },
            { value: '3', label: '3 = น้ำนิ่ง/น้ำทรง (Slack water)' }
        ]},
        { key: 'f3_tide_extreme', label: 'เสี่ยงน้ำลงแห้งขอดจัด (< 1.0 ม.)', form: 3, formName: 'Form 3', category: 'อุทกศาสตร์ทางทะเล', type: 'select', options: [
            { value: '0', label: '0 = ปกติ (ระดับน้ำ ≥ 1.0 ม.)' },
            { value: '1', label: '1 = เสี่ยงน้ำแห้งขอดจัด (< 1.0 ม.)' }
        ]},
        { key: 'f3_sandbar_risk', label: 'ความเสี่ยงสันทรายท่าเรือ (Sandbar Risk)', form: 3, formName: 'Form 3', category: 'อุทกศาสตร์ทางทะเล', type: 'select', options: [
            { value: '0', label: '0 = ไม่มีสันทรายขวางร่องน้ำ' },
            { value: '1', label: '1 = มีความเสี่ยงติดสันทราย' }
        ]},

        // สภาพอากาศและคลื่นลม
        { key: 'f3_season', label: 'ฤดูกาลมรสุม (Monsoon Season)', form: 3, formName: 'Form 3', category: 'สภาพอากาศและคลื่นลม', type: 'select', options: [
            { value: '0', label: '0 = ฤดูมรสุมตะวันตกเฉียงใต้ (พ.ค.–ต.ค.)' },
            { value: '1', label: '1 = นอกฤดูมรสุม / ไฮซีซั่น (พ.ย.–เม.ย.)' }
        ]},
        { key: 'f3_sea_state', label: 'ระดับคลื่นลมทะเล (Beaufort Sea State)', form: 3, formName: 'Form 3', category: 'สภาพอากาศและคลื่นลม', type: 'select', options: [
            { value: '0', label: '0 = Calm (คลื่นสงบ ≤ 1.0 ม.)' },
            { value: '1', label: '1 = Moderate (คลื่นปานกลาง 1.0–2.0 ม.)' },
            { value: '2', label: '2 = Rough (คลื่นลมแรงมรสุม > 2.0 ม.)' }
        ]},
        { key: 'f3_precipitation', label: 'สภาพฝนตก (Precipitation)', form: 3, formName: 'Form 3', category: 'สภาพอากาศและคลื่นลม', type: 'select', options: [
            { value: '0', label: '0 = อากาศแจ่มใส / ไม่มีฝน หรือฝนเล็กน้อย' },
            { value: '1', label: '1 = ฝนตกหนัก / พายุฝน' }
        ]},
        { key: 'f3_rainfall_mm', label: 'ปริมาณน้ำฝนสะสมรายชั่วโมง (mm/hr)', form: 3, formName: 'Form 3', category: 'สภาพอากาศและคลื่นลม', type: 'number', unit: 'มม./ชม.', step: '0.1', condition: d => d.f3_precipitation === '1' },
        { key: 'f3_torrential_rain', label: 'เกณฑ์พายุฝนตกหนักวิกฤต', form: 3, formName: 'Form 3', category: 'สภาพอากาศและคลื่นลม', type: 'select', condition: d => d.f3_precipitation === '1', options: [
            { value: '0', label: '0 = ไม่เข้าเกณฑ์พายุฝนหนัก' },
            { value: '1', label: '1 = พายุฝนตกหนักวิกฤต (≥ 10 มม./ชม. หรือ ≥ 35 มม./วัน)' }
        ]},
        { key: 'f3_holiday', label: 'ช่วงวันหยุดยาว / เทศกาลท่องเที่ยว', form: 3, formName: 'Form 3', category: 'สภาพอากาศและคลื่นลม', type: 'select', options: [
            { value: '0', label: '0 = วันธรรมดา (จันทร์–ศุกร์)' },
            { value: '1', label: '1 = วันหยุดยาวราชการ ≥ 3 วัน / เทศกาล' }
        ]},
        { key: 'f3_ferry_shift', label: 'กะการเดินแพขนานยนต์ (Ferry Shift)', form: 3, formName: 'Form 3', category: 'สภาพอากาศและคลื่นลม', type: 'select', options: [
            { value: '0', label: '0 = Scheduled Daytime (05:00–24:00 น.) เดินแพปกติ' },
            { value: '1', label: '1 = Standby Off-Hour (24:00–05:00 น.) โทรตามแพพิเศษ' }
        ]},
        { key: 'f3_ed_shift', label: 'ช่วงเวรการทำงานห้องฉุกเฉิน (Form 3)', form: 3, formName: 'Form 3', category: 'สภาพอากาศและคลื่นลม', type: 'select', options: [
            { value: 'morning', label: 'เวรเช้า (08:00–16:00 น.)' },
            { value: 'afternoon', label: 'เวรบ่าย (16:00–24:00 น.)' },
            { value: 'night', label: 'เวรดึก (00:00–08:00 น.)' }
        ]},

        // การตรวจสอบแหล่งอ้างอิง
        { key: 'f3_ref_rtn_date', label: 'วันที่สืบค้นข้อมูล RTN', form: 3, formName: 'Form 3', category: 'การตรวจสอบแหล่งอ้างอิง', type: 'date' },
        { key: 'f3_ref_tmd_date', label: 'วันที่สืบค้นข้อมูล TMD', form: 3, formName: 'Form 3', category: 'การตรวจสอบแหล่งอ้างอิง', type: 'date' },

        // ==========================================
        // Form 4: การรักษา ณ รพ.กระบี่ และผลลัพธ์ 24 ชม.
        // ==========================================
        // แรกรับ รพ.กระบี่
        { key: 'f4_krabi_hn', label: 'เลข HN รพ.กระบี่', form: 4, formName: 'Form 4', category: 'แรกรับ รพ.กระบี่', type: 'text', placeholder: 'HN รพ.กระบี่' },
        { key: 'f4_physician', label: 'ชื่อแพทย์เจ้าของไข้ รพ.กระบี่', form: 4, formName: 'Form 4', category: 'แรกรับ รพ.กระบี่', type: 'text', placeholder: 'ชื่อ-สกุล แพทย์เจ้าของไข้' },
        { key: 'f4_ward', label: 'หอผู้ป่วยรับไว้รักษาแรกรับ', form: 4, formName: 'Form 4', category: 'แรกรับ รพ.กระบี่', type: 'select', options: [
            { value: 'ccu', label: 'CCU (Coronary Care Unit)' },
            { value: 'stroke', label: 'Stroke Unit' },
            { value: 'sicu', label: 'Trauma ICU / SICU' },
            { value: 'general', label: 'หอผู้ป่วยสามัญ (General Ward)' }
        ]},

        // สัญญาณชีพแรกรับกระบี่
        { key: 'f4_sbp', label: 'SBP แรกรับ รพ.กระบี่', form: 4, formName: 'Form 4', category: 'สัญญาณชีพแรกรับกระบี่', type: 'number', unit: 'mmHg' },
        { key: 'f4_dbp', label: 'DBP แรกรับ รพ.กระบี่', form: 4, formName: 'Form 4', category: 'สัญญาณชีพแรกรับกระบี่', type: 'number', unit: 'mmHg' },
        { key: 'f4_hr', label: 'ชีพจรแรกรับกระบี่ (Heart Rate)', form: 4, formName: 'Form 4', category: 'สัญญาณชีพแรกรับกระบี่', type: 'number', unit: 'bpm' },
        { key: 'f4_rr', label: 'อัตราหายใจแรกรับกระบี่ (Resp Rate)', form: 4, formName: 'Form 4', category: 'สัญญาณชีพแรกรับกระบี่', type: 'number', unit: '/min' },
        { key: 'f4_spo2', label: 'ออกซิเจนในเลือดแรกรับกระบี่ (SpO2)', form: 4, formName: 'Form 4', category: 'สัญญาณชีพแรกรับกระบี่', type: 'number', unit: '%' },
        { key: 'f4_bt', label: 'อุณหภูมิกายแรกรับกระบี่ (Body Temp)', form: 4, formName: 'Form 4', category: 'สัญญาณชีพแรกรับกระบี่', type: 'number', unit: '°C', step: '0.1' },
        { key: 'f4_hct', label: 'ความเข้มข้นเลือด (Hct แรกรับกระบี่)', form: 4, formName: 'Form 4', category: 'สัญญาณชีพแรกรับกระบี่', type: 'number', unit: '%', step: '0.1' },
        { key: 'f4_gcs_total', label: 'คะแนน GCS แรกรับกระบี่', form: 4, formName: 'Form 4', category: 'สัญญาณชีพแรกรับกระบี่', type: 'number', unit: 'คะแนน', min: 3, max: 15 },

        // ความรุนแรงแรกรับกระบี่ (จำเพาะโรค)
        { key: 'f4_killip', label: 'STEMI Killip Class ณ รพ.กระบี่', form: 4, formName: 'Form 4', category: 'ความรุนแรงแรกรับกระบี่', type: 'select', condition: isCaseStemi, options: [
            { value: '1_2', label: 'Killip Class I, II' },
            { value: '3', label: 'Killip Class III' },
            { value: '4', label: 'Killip Class IV' }
        ]},
        { key: 'f4_stroke_gcs', label: 'Stroke GCS ณ รพ.กระบี่', form: 4, formName: 'Form 4', category: 'ความรุนแรงแรกรับกระบี่', type: 'select', condition: isCaseStroke, options: [
            { value: 'severe', label: 'GCS 3–8 (Severe Coma)' },
            { value: 'moderate', label: 'GCS 9–12 (Moderate)' },
            { value: 'mild', label: 'GCS 13–15 (Mild)' }
        ]},
        { key: 'f4_trauma_acuity', label: 'Trauma Acuity ณ รพ.กระบี่', form: 4, formName: 'Form 4', category: 'ความรุนแรงแรกรับกระบี่', type: 'select', condition: isCaseTrauma, options: [
            { value: 'critical', label: 'RTS ≤ 6 (Critical)' },
            { value: 'moderate', label: 'RTS > 6 (Moderate)' }
        ]},

        // การประเมินภาวะทรุดหนักสรีรวิทยา
        { key: 'f4_eval_killip', label: 'การประเมิน ΔKillip (STEMI)', form: 4, formName: 'Form 4', category: 'การประเมินภาวะทรุดหนักสรีรวิทยา', type: 'select', condition: isCaseStemi, options: [
            { value: 'stable', label: 'คงที่ / ดีขึ้น' },
            { value: 'deter', label: 'ทรุดหนัก (ΔKillip ≥ +1 หรือดำเนินสู่ Class IV)' }
        ]},
        { key: 'f4_eval_gcs', label: 'การประเมิน ΔGCS (Neurological)', form: 4, formName: 'Form 4', category: 'การประเมินภาวะทรุดหนักสรีรวิทยา', type: 'select', options: [
            { value: 'stable', label: 'คงที่ / ดีขึ้น' },
            { value: 'deter', label: 'ทรุดหนัก (ΔGCS ≤ -2)' }
        ]},
        { key: 'f4_eval_rts', label: 'การประเมิน ΔRTS (Trauma)', form: 4, formName: 'Form 4', category: 'การประเมินภาวะทรุดหนักสรีรวิทยา', type: 'select', condition: isCaseTrauma, options: [
            { value: 'stable', label: 'คงที่ / ดีขึ้น' },
            { value: 'deter', label: 'ทรุดหนัก (ΔRTS ≤ -1.0)' }
        ]},
        { key: 'f4_eval_msi', label: 'การประเมิน ΔMSI (STEMI)', form: 4, formName: 'Form 4', category: 'การประเมินภาวะทรุดหนักสรีรวิทยา', type: 'select', condition: isCaseStemi, options: [
            { value: 'stable', label: 'คงที่ / ปกติ' },
            { value: 'deter', label: 'ทรุดหนัก (ΔMSI ≥ +0.15)' }
        ]},
        { key: 'f4_eval_map', label: 'การประเมิน ΔMAP (Hemodynamic)', form: 4, formName: 'Form 4', category: 'การประเมินภาวะทรุดหนักสรีรวิทยา', type: 'select', options: [
            { value: 'stable', label: 'คงที่ (MAP เพิ่มขึ้นหรือ ≥ 65 mmHg)' },
            { value: 'deter', label: 'ทรุดหนัก (MAP ลดลง และ < 65 mmHg)' }
        ]},
        { key: 'f4_eval_bt', label: 'การประเมิน ΔBT (Temperature)', form: 4, formName: 'Form 4', category: 'การประเมินภาวะทรุดหนักสรีรวิทยา', type: 'select', options: [
            { value: 'normal', label: 'ปกติ' },
            { value: 'hypothermia', label: 'เกิด Hypothermia (< 35 °C)' }
        ]},
        { key: 'f4_composite_deter', label: 'สรุปภาวะทรุดหนักสรีรวิทยารวม', form: 4, formName: 'Form 4', category: 'การประเมินภาวะทรุดหนักสรีรวิทยา', type: 'select', options: [
            { value: '0', label: '0 = สัญญาณชีพคงที่ตลอดการส่งต่อ (Stable)' },
            { value: '1', label: '1 = เกิดภาวะทรุด (Deteriorated)' }
        ]},

        // หัตถการจำเพาะและกรอบเวลา (T5)
        { key: 'f4_t5_date', label: 'วันที่เริ่มทำหัตถการรักษาจำเพาะ T5', form: 4, formName: 'Form 4', category: 'หัตถการจำเพาะและกรอบเวลา (T5)', type: 'date' },
        { key: 'f4_t5_time', label: 'เวลาเริ่มทำหัตถการรักษาจำเพาะ T5', form: 4, formName: 'Form 4', category: 'หัตถการจำเพาะและกรอบเวลา (T5)', type: 'time' },
        { key: 'f4_pci_wire_time', label: 'เวลาลวดผ่านรอยโรค Primary PCI (T5 Time)', form: 4, formName: 'Form 4', category: 'หัตถการจำเพาะและกรอบเวลา (T5)', type: 'time', condition: isCaseStemi },
        { key: 'f4_eval_pci', label: 'การบรรลุเกณฑ์ Remote Primary PCI', form: 4, formName: 'Form 4', category: 'หัตถการจำเพาะและกรอบเวลา (T5)', type: 'select', condition: isCaseStemi, options: [
            { value: 'achieved', label: 'บรรลุเกณฑ์ Remote Primary PCI (≤ 180 นาที)' },
            { value: 'missed', label: 'หลุดกรอบเวลา (STEMI PCI > 180 นาที)' }
        ]},
        { key: 'f4_rtpa_time', label: 'เวลาเริ่มฉีดยา rtPA Bolus (T5 Time)', form: 4, formName: 'Form 4', category: 'หัตถการจำเพาะและกรอบเวลา (T5)', type: 'time', condition: isCaseStroke },
        { key: 'f4_ct_brain_time', label: 'เวลาทำ CT Brain เสร็จสิ้น', form: 4, formName: 'Form 4', category: 'หัตถการจำเพาะและกรอบเวลา (T5)', type: 'time', condition: isCaseStroke },
        { key: 'f4_eval_stroke', label: 'การบรรลุเกณฑ์ IV rtPA', form: 4, formName: 'Form 4', category: 'หัตถการจำเพาะและกรอบเวลา (T5)', type: 'select', condition: isCaseStroke, options: [
            { value: 'achieved', label: 'บรรลุเกณฑ์ IV rtPA (≤ 4.5 ชั่วโมง)' },
            { value: 'missed', label: 'หลุดกรอบเวลา (Stroke rtPA > 4.5 ชั่วโมง)' }
        ]},
        { key: 'f4_trauma_ct_time', label: 'เวลาทำ CT Scan บาดเจ็บเสร็จสิ้น', form: 4, formName: 'Form 4', category: 'หัตถการจำเพาะและกรอบเวลา (T5)', type: 'time', condition: isCaseTrauma },
        { key: 'f4_or_time', label: 'เวลาลงมีดผ่าตัดฉุกเฉิน (Damage Control OR)', form: 4, formName: 'Form 4', category: 'หัตถการจำเพาะและกรอบเวลา (T5)', type: 'time', condition: isCaseTrauma },
        { key: 'f4_eval_trauma', label: 'การบรรลุเกณฑ์ Trauma Golden Window', form: 4, formName: 'Form 4', category: 'หัตถการจำเพาะและกรอบเวลา (T5)', type: 'select', condition: isCaseTrauma, options: [
            { value: 'achieved', label: 'บรรลุเกณฑ์ตามเวลา (OR ≤ 180 น. หรือ CT ≤ 150 น.)' },
            { value: 'missed', label: 'หลุดกรอบเวลา (OR > 180 น. หรือ CT > 150 น.)' }
        ]},

        // ผลลัพธ์การรักษาและรอดชีวิต
        { key: 'f4_mort_er', label: 'การเสียชีวิตทันที ณ ห้องฉุกเฉิน รพ.กระบี่', form: 4, formName: 'Form 4', category: 'ผลลัพธ์การรักษาและรอดชีวิต', type: 'select', options: [
            { value: '0', label: '0 = รอดชีวิตผ่านพ้นห้องฉุกเฉิน' },
            { value: '1', label: '1 = เสียชีวิตทันที ณ ห้องฉุกเฉิน' }
        ]},
        { key: 'f4_mort_er_time', label: 'เวลาเสียชีวิต ณ ห้องฉุกเฉิน รพ.กระบี่', form: 4, formName: 'Form 4', category: 'ผลลัพธ์การรักษาและรอดชีวิต', type: 'time', condition: d => d.f4_mort_er === '1' },
        { key: 'f4_mort_24h', label: 'ผลลัพธ์การรอดชีวิตที่ 24 ชม. หลังรับไว้รักษา', form: 4, formName: 'Form 4', category: 'ผลลัพธ์การรักษาและรอดชีวิต', type: 'select', options: [
            { value: '0', label: '0 = รอดชีวิตเกิน 24 ชั่วโมงแรก' },
            { value: '1', label: '1 = เสียชีวิตภายใน 24 ชั่วโมงแรก' }
        ]},
        { key: 'f4_mort_24h_date', label: 'วันที่เสียชีวิตภายใน 24 ชม.', form: 4, formName: 'Form 4', category: 'ผลลัพธ์การรักษาและรอดชีวิต', type: 'date', condition: d => d.f4_mort_24h === '1' },
        { key: 'f4_mort_24h_time', label: 'เวลาเสียชีวิตภายใน 24 ชม.', form: 4, formName: 'Form 4', category: 'ผลลัพธ์การรักษาและรอดชีวิต', type: 'time', condition: d => d.f4_mort_24h === '1' },
        { key: 'f4_mort_cause', label: 'สาเหตุการเสียชีวิตหลัก', form: 4, formName: 'Form 4', category: 'ผลลัพธ์การรักษาและรอดชีวิต', type: 'select', condition: d => d.f4_mort_er === '1' || d.f4_mort_24h === '1', options: [
            { value: 'stemi', label: 'Cardiogenic shock / Malignant ventricular arrhythmia (STEMI)' },
            { value: 'stroke', label: 'Massive cerebral infarction / Intracranial hemorrhage / Herniation (Acute Stroke)' },
            { value: 'trauma', label: 'Exsanguinating hemorrhagic shock / Coagulopathy (Severe Trauma)' },
            { value: 'other', label: 'อื่นๆ ระบุ (ICD-10)' }
        ]},
        { key: 'f4_mort_cause_icd', label: 'ระบุสาเหตุการเสียชีวิต (ICD-10)', form: 4, formName: 'Form 4', category: 'ผลลัพธ์การรักษาและรอดชีวิต', type: 'text', condition: d => (d.f4_mort_er === '1' || d.f4_mort_24h === '1') && d.f4_mort_cause === 'other', placeholder: 'รหัส ICD-10 หรือคำวินิจฉัย' }
    ];

    function getCaseMissingFields(data) {
        if (!data) return [];
        const isExcluded = (data.f1_eligible === 'excluded');
        const missing = [];
        CRF_AUDIT_FIELDS.forEach(field => {
            if (isExcluded && (field.form > 1 || (field.category !== 'ข้อมูลทั่วไปและผู้สกัด' && field.category !== 'เกณฑ์การคัดกรองวิจัย'))) return;
            if (field.condition && !field.condition(data)) return;
            if (!isFieldFilled(data, field.key)) {
                missing.push(field);
            }
        });
        return missing;
    }

    function getCaseCompleteness(data) {
        if (!data) return { totalExpected: 0, filledCount: 0, missingCount: 0, pct: 100, missingFields: [], byForm: { 1: { expected: 0, missing: [] }, 2: { expected: 0, missing: [] }, 3: { expected: 0, missing: [] }, 4: { expected: 0, missing: [] } } };
        const isExcluded = (data.f1_eligible === 'excluded');
        let totalExpected = 0;
        const missingFields = [];
        const byForm = { 1: { expected: 0, missing: [] }, 2: { expected: 0, missing: [] }, 3: { expected: 0, missing: [] }, 4: { expected: 0, missing: [] } };

        CRF_AUDIT_FIELDS.forEach(field => {
            if (isExcluded && (field.form > 1 || (field.category !== 'ข้อมูลทั่วไปและผู้สกัด' && field.category !== 'เกณฑ์การคัดกรองวิจัย'))) return;
            if (field.condition && !field.condition(data)) return;

            totalExpected++;
            if (byForm[field.form]) byForm[field.form].expected++;

            if (!isFieldFilled(data, field.key)) {
                missingFields.push(field);
                if (byForm[field.form]) byForm[field.form].missing.push(field);
            }
        });

        const missingCount = missingFields.length;
        const filledCount = totalExpected - missingCount;
        const pct = totalExpected > 0 ? Math.round((filledCount / totalExpected) * 100) : 100;

        return {
            totalExpected,
            filledCount,
            missingCount,
            pct,
            missingFields,
            byForm,
            isExcluded
        };
    }

    // --- Admin Table Sorting State & Handlers ---
    let adminSortColumn = 'studyId';
    let adminSortDirection = 'asc';

    function handleAdminTableSort(columnKey) {
        if (adminSortColumn === columnKey) {
            adminSortDirection = (adminSortDirection === 'asc') ? 'desc' : 'asc';
        } else {
            adminSortColumn = columnKey;
            if (columnKey === 'completeness' || columnKey === 'transferTime') {
                adminSortDirection = 'desc';
            } else {
                adminSortDirection = 'asc';
            }
        }
        renderAdminDashboard();
    }
    if (typeof window !== 'undefined') {
        window.handleAdminTableSort = handleAdminTableSort;
    }

    function compareSortable(valA, valB, isNumeric = false) {
        const isEmptyA = (valA === null || valA === undefined || valA === '');
        const isEmptyB = (valB === null || valB === undefined || valB === '');
        if (isEmptyA && isEmptyB) return 0;
        if (isEmptyA) return 1;  // empty A stays at bottom
        if (isEmptyB) return -1; // empty B stays at bottom

        let res = 0;
        if (isNumeric) {
            res = Number(valA) - Number(valB);
        } else {
            res = String(valA).localeCompare(String(valB), 'th', { numeric: true, sensitivity: 'base' });
        }
        return adminSortDirection === 'asc' ? res : -res;
    }

    function compareAdminCases(a, b) {
        switch (adminSortColumn) {
            case 'studyId': {
                const numA = parseInt(a.studyId, 10);
                const numB = parseInt(b.studyId, 10);
                const isNumA = !isNaN(numA);
                const isNumB = !isNaN(numB);
                if (isNumA && isNumB) return compareSortable(numA, numB, true);
                return compareSortable(a.studyId, b.studyId, false);
            }
            case 'hn': {
                const strA = (a.hn && a.hn !== '-' ? a.hn : '') || a.referId || '';
                const strB = (b.hn && b.hn !== '-' ? b.hn : '') || b.referId || '';
                return compareSortable(strA, strB, false);
            }
            case 'age': {
                const ageA = a.age ? parseFloat(a.age) : null;
                const ageB = b.age ? parseFloat(b.age) : null;
                return compareSortable(ageA, ageB, true);
            }
            case 'esi': {
                const esiA = a.esi ? parseInt(a.esi, 10) : null;
                const esiB = b.esi ? parseInt(b.esi, 10) : null;
                return compareSortable(esiA, esiB, true);
            }
            case 'disease': {
                const disA = a.isStemi ? 'STEMI' : (a.isStroke ? 'Stroke' : (a.isTrauma ? 'Trauma' : (a.diseaseKey || null)));
                const disB = b.isStemi ? 'STEMI' : (b.isStroke ? 'Stroke' : (b.isTrauma ? 'Trauma' : (b.diseaseKey || null)));
                return compareSortable(disA, disB, false);
            }
            case 'transferTime': {
                const tA = (!isNaN(a.transferMin) && a.transferMin > 0) ? a.transferMin : null;
                const tB = (!isNaN(b.transferMin) && b.transferMin > 0) ? b.transferMin : null;
                return compareSortable(tA, tB, true);
            }
            case 'rts': {
                const rtsA = !isNaN(parseFloat(a.data?.f1_rts_total)) ? parseFloat(a.data.f1_rts_total) : (!isNaN(parseFloat(a.data?.f4_rts_total)) ? parseFloat(a.data.f4_rts_total) : null);
                const rtsB = !isNaN(parseFloat(b.data?.f1_rts_total)) ? parseFloat(b.data.f1_rts_total) : (!isNaN(parseFloat(b.data?.f4_rts_total)) ? parseFloat(b.data.f4_rts_total) : null);
                return compareSortable(rtsA, rtsB, true);
            }
            case 'outcome': {
                const getRank = c => {
                    const d = c.data || {};
                    const st = d.f4_mort_status !== undefined && d.f4_mort_status !== '' ? d.f4_mort_status : (d.f4_mort_24h !== undefined && d.f4_mort_24h !== '' ? d.f4_mort_24h : d.f4_mort_er);
                    if (st === '0') return 1; // รอดชีวิต
                    if (st === '1') return 2; // เสียชีวิต
                    return null; // รอผล / ไม่ระบุ
                };
                return compareSortable(getRank(a), getRank(b), true);
            }
            case 'completeness': {
                const pctA = a.completeness ? a.completeness.pct : null;
                const pctB = b.completeness ? b.completeness.pct : null;
                return compareSortable(pctA, pctB, true);
            }
            default:
                return 0;
        }
    }

    function updateAdminSortIndicators() {
        const sortKeys = ['studyId', 'hn', 'age', 'esi', 'disease', 'transferTime', 'rts', 'outcome', 'completeness'];
        sortKeys.forEach(key => {
            const iconEl = document.getElementById('th-sort-' + key);
            const thEl = document.querySelector(`.admin-th-sortable[data-sort="${key}"]`);
            if (key === adminSortColumn) {
                if (iconEl) {
                    iconEl.textContent = adminSortDirection === 'asc' ? '▲' : '▼';
                    iconEl.style.opacity = '1';
                    iconEl.style.color = '#1d4ed8';
                }
                if (thEl) thEl.classList.add('active-sort');
            } else {
                if (iconEl) {
                    iconEl.textContent = '⇅';
                    iconEl.style.opacity = '0.4';
                    iconEl.style.color = '#64748b';
                }
                if (thEl) thEl.classList.remove('active-sort');
            }
        });
    }

    // Main Render Function for Research Admin Dashboard
    function renderAdminDashboard() {
        const index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
        const tbody = document.getElementById('admin-cases-tbody');
        if (!tbody) return;

        // Load and parse all cases
        const allCases = [];
        index.forEach(studyId => {
            const raw = localStorage.getItem('online_crf_case_' + studyId);
            if (!raw) return;
            try {
                const data = JSON.parse(raw);
                const isStemi = Boolean(data.f1_target_disease === 'stemi' || data.f1_inc4_stemi || data.f1_cond_stemi);
                const isStroke = Boolean(data.f1_target_disease === 'ais' || data.f1_inc4_ais || data.f1_cond_stroke);
                const isTrauma = Boolean(data.f1_target_disease === 'trauma' || data.f1_inc4_trauma || data.f1_cond_trauma);
                const diseaseKey = isStemi ? 'stemi' : (isStroke ? 'ais' : (isTrauma ? 'trauma' : 'other'));
                const esi = String(data.f1_esi || data.f1_triage_esi || '');
                const transferMin = parseFloat(data.f2_t_total_min || data.f2_eq1_total_transfer);
                const isExposed = checkCaseExposure(data);

                const hasCpr = Boolean(data.f2_ae_cpr === '1');
                const hasIntub = Boolean(data.f2_ae_intub === '1');
                const hasInotropes = Boolean(data.f2_ae_inotropes === '1');
                const hasDislodge = Boolean(data.f2_ae_dislodge === '1');
                const hasTransitDeath = Boolean(data.f2_ae_death === '1');
                const hasTransitAE = Boolean(data.f2_composite_ae === '1' || hasCpr || hasIntub || hasInotropes || hasDislodge || hasTransitDeath);

                const deltaGcsVal = data.f4_delta_gcs ? parseInt(data.f4_delta_gcs, 10) : null;
                const hasGcsDeter = Boolean(data.f4_eval_gcs === 'deter' || (deltaGcsVal !== null && deltaGcsVal <= -2));

                const sbpKbh = data.f4_sbp ? parseFloat(data.f4_sbp) : null;
                const deltaSbp = data.f4_delta_sbp ? parseFloat(data.f4_delta_sbp) : null;
                const hasMapDeter = Boolean(data.f4_eval_map === 'deter' || (sbpKbh !== null && sbpKbh < 90 && deltaSbp !== null && deltaSbp < 0));

                const btVal = data.f4_bt ? parseFloat(data.f4_bt) : null;
                const hasHypo = Boolean(data.f4_eval_bt === 'hypothermia' || (btVal !== null && btVal < 35.0));

                const hasKillip = Boolean(isStemi && (data.f4_eval_killip === 'deter' || data.f4_delta_killip_to === '4'));
                const hasMsi = Boolean(isStemi && (data.f4_eval_msi === 'deter' || (data.f4_delta_msi && parseFloat(data.f4_delta_msi) >= 0.15)));
                const hasRts = Boolean(isTrauma && (data.f4_eval_rts === 'deter' || (data.f4_delta_rts && parseFloat(data.f4_delta_rts) <= -1.0)));

                const hasPhysioDeter = Boolean(data.f4_composite_deter === '1' || hasGcsDeter || hasMapDeter || hasHypo || hasKillip || hasMsi || hasRts);
                const isDeteriorated = Boolean(hasTransitAE || hasPhysioDeter);

                const t0ToT1 = parseFloat(data.f2_eq2_dido || data.f2_t0_1_min);
                const t2ToT3 = parseFloat(data.f2_eq4_pier_wait || data.f2_t2_3_min);
                const t3Dur = parseFloat(data.f2_eq5_ferry_cross || data.f2_t3_cross_min);
                const t4Dur = parseFloat(data.f2_eq6_mainland_road || data.f2_t4_mainland_min);
                const t4ToT5 = parseFloat(data.f4_t4_5_min);

                allCases.push({
                    studyId: studyId,
                    displayId: 'LANTA_' + studyId,
                    hn: data.f1_hn || '-',
                    referId: data.f1_refer_id || '-',
                    age: data.f1_age || '',
                    sex: data.f1_sex || '',
                    esi: esi,
                    isStemi: isStemi,
                    isStroke: isStroke,
                    isTrauma: isTrauma,
                    diseaseKey: diseaseKey,
                    transferMin: transferMin,
                    isExposed: isExposed,
                    hasCpr: hasCpr,
                    hasIntub: hasIntub,
                    hasInotropes: hasInotropes,
                    hasDislodge: hasDislodge,
                    hasTransitDeath: hasTransitDeath,
                    hasTransitAE: hasTransitAE,
                    hasGcsDeter: hasGcsDeter,
                    hasMapDeter: hasMapDeter,
                    hasHypo: hasHypo,
                    hasKillip: hasKillip,
                    hasMsi: hasMsi,
                    hasRts: hasRts,
                    hasPhysioDeter: hasPhysioDeter,
                    isDeteriorated: isDeteriorated,
                    t0ToT1: isNaN(t0ToT1) ? null : t0ToT1,
                    t2ToT3: isNaN(t2ToT3) ? null : t2ToT3,
                    t3Dur: isNaN(t3Dur) ? null : t3Dur,
                    t4Dur: isNaN(t4Dur) ? null : t4Dur,
                    t4ToT5: isNaN(t4ToT5) ? null : t4ToT5,
                    completeness: getCaseCompleteness(data),
                    data: data
                });
            } catch(e) {}
        });

        // Read active filters
        const filterDisease = document.getElementById('admin-filter-disease')?.value || '';
        const filterEsi = document.getElementById('admin-filter-esi')?.value || '';
        const filterCohort = document.getElementById('admin-filter-cohort')?.value || '';
        const query = (document.getElementById('admin-search-box')?.value || '').toLowerCase().trim();

        // Filter cases
        const filtered = allCases.filter(c => {
            if (filterDisease && c.diseaseKey !== filterDisease) return false;
            if (filterEsi && c.esi !== filterEsi) return false;
            if (filterCohort === 'exposed' && !c.isExposed) return false;
            if (filterCohort === 'unexposed' && c.isExposed) return false;
            if (query) {
                const matchId = c.displayId.toLowerCase().includes(query) || c.studyId.toLowerCase().includes(query);
                const matchHn = c.hn.toLowerCase().includes(query);
                const matchRef = c.referId.toLowerCase().includes(query);
                if (!matchId && !matchHn && !matchRef) return false;
            }
            return true;
        });

        // Sort cases according to active column & direction
        filtered.sort(compareAdminCases);

        // Update global filter badges
        const badgeCount = document.getElementById('admin-filter-count-badge');
        const badgeTotal = document.getElementById('admin-total-cases-badge');
        if (badgeCount) badgeCount.textContent = filtered.length;
        if (badgeTotal) badgeTotal.textContent = allCases.length;

        // Completeness & Missing Fields Statistics
        let totalAuditExpected = 0;
        let totalAuditFilled = 0;
        let totalAuditMissing = 0;
        let missingByForm = { 1: 0, 2: 0, 3: 0, 4: 0 };
        let expectedByForm = { 1: 0, 2: 0, 3: 0, 4: 0 };

        filtered.forEach(c => {
            const comp = c.completeness;
            if (comp) {
                totalAuditExpected += comp.totalExpected;
                totalAuditFilled += comp.filledCount;
                totalAuditMissing += comp.missingCount;
                for (let f = 1; f <= 4; f++) {
                    if (comp.byForm && comp.byForm[f]) {
                        expectedByForm[f] += comp.byForm[f].expected;
                        missingByForm[f] += comp.byForm[f].missing.length;
                    }
                }
            }
        });
        const overallCompletenessPct = totalAuditExpected > 0 ? Math.round((totalAuditFilled / totalAuditExpected) * 100) : 100;

        // =====================================================================
        // TAB 1: OVERVIEW & CASE DIRECTORY
        // =====================================================================
        let totalPatients = filtered.length;
        let totalTransferMinutes = 0;
        let transferTimeCount = 0;
        let esi1Count = 0;
        let survivalCount = 0;
        let mortalityAssessedCount = 0;

        let diseaseCounts = { stemi: 0, stroke: 0, trauma: 0, other: 0 };
        let timelinessCounts = { ontime: 0, delay: 0, unknown: 0 };
        let outcomeCounts = { survive: 0, death: 0, pending: 0 };
        let esiCounts = { esi1: 0, esi2: 0, esi3: 0, other: 0 };

        let rowsHtml = '';

        if (filtered.length === 0) {
            tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; padding: 25px; color: #64748b; font-size: 14px;">ไม่พบข้อมูลเคสที่ตรงกับเงื่อนไขตัวกรอง (หรือยังไม่มีข้อมูลในระบบ)</td></tr>';
        } else {
            filtered.forEach(c => {
                const data = c.data;
                const esi = c.esi;
                if (esi === '1') { esi1Count++; esiCounts.esi1++; }
                else if (esi === '2') esiCounts.esi2++;
                else if (esi === '3') esiCounts.esi3++;
                else esiCounts.other++;

                if (!isNaN(c.transferMin) && c.transferMin > 0) {
                    totalTransferMinutes += c.transferMin;
                    transferTimeCount++;
                    if (c.transferMin <= 180) timelinessCounts.ontime++;
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

                if (c.isStemi) diseaseCounts.stemi++;
                else if (c.isStroke) diseaseCounts.stroke++;
                else if (c.isTrauma) diseaseCounts.trauma++;
                else diseaseCounts.other++;

                // Table row generation
                const ageStr = c.age ? c.age + ' ปี' : '-';
                const sexStr = (c.sex === '1' || c.sex === 'male') ? 'ชาย' : ((c.sex === '2' || c.sex === 'female') ? 'หญิง' : '-');

                let esiBadge = '-';
                if (esi === '1') esiBadge = '<span class="badge-evaluated" style="background:#fee2e2; color:#b91c1c; font-size:11px;">ESI 1</span>';
                else if (esi === '2') esiBadge = '<span class="badge-evaluated" style="background:#ffedd5; color:#c2410c; font-size:11px;">ESI 2</span>';
                else if (esi === '3') esiBadge = '<span class="badge-evaluated" style="background:#fef9c3; color:#a16207; font-size:11px;">ESI 3</span>';
                else if (esi) esiBadge = '<span class="badge-evaluated" style="background:#f1f5f9; color:#475569; font-size:11px;">ESI ' + esi + '</span>';

                const conds = [];
                if (c.isStemi) conds.push('<span style="background:#fee2e2; color:#991b1b; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:600;">STEMI</span>');
                if (c.isStroke) conds.push('<span style="background:#fef3c7; color:#92400e; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:600;">Stroke</span>');
                if (c.isTrauma) conds.push('<span style="background:#ede9fe; color:#5b21b6; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:600;">Trauma</span>');
                if (data.f1_cond_sepsis) conds.push('<span style="background:#e0e7ff; color:#3730a3; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:600;">Sepsis</span>');
                if (data.f1_cond_arrest) conds.push('<span style="background:#fce7f3; color:#9d174d; padding:1px 6px; border-radius:4px; font-size:11px; font-weight:600;">Arrest</span>');
                const condHtml = conds.length > 0 ? conds.join(' ') : '<span style="color:#94a3b8;">-</span>';

                let transferHtml = '-';
                if (!isNaN(c.transferMin) && c.transferMin > 0) {
                    const isDelay = c.transferMin > 180;
                    transferHtml = '<b>' + c.transferMin + '</b> น. ' + (isDelay ? '<span class="badge-evaluated badge-delay" style="font-size:10px;">ล่าช้า</span>' : '<span class="badge-evaluated badge-ontime" style="font-size:10px;">ตามเกณฑ์</span>');
                }

                let rtsHtml = '-';
                if (c.isTrauma) {
                    const rts1 = data.f1_rts_total || '-';
                    const rts4 = data.f4_rts_total || '-';
                    rtsHtml = rts1 + ' ➔ ' + rts4;
                } else if (c.isStroke) rtsHtml = '<span style="color:#94a3b8; font-size:11px;">(Stroke: N/A)</span>';
                else if (c.isStemi) rtsHtml = '<span style="color:#94a3b8; font-size:11px;">(STEMI: N/A)</span>';

                let outcomeHtml = '<span style="color:#94a3b8;">รอผล</span>';
                if (mortStatus === '0') outcomeHtml = '<span class="badge-evaluated badge-ontime" style="background:#dcfce7; color:#15803d; font-size:11px;">✓ รอดชีวิต</span>';
                else if (mortStatus === '1') outcomeHtml = '<span class="badge-evaluated badge-delay" style="background:#fee2e2; color:#b91c1c; font-size:11px;">✕ เสียชีวิต</span>';

                const ineligBadge = (data.f1_eligible === 'excluded') ? '<div style="font-size: 10px; color: #dc2626; font-weight: 700; background: #fee2e2; border-radius: 4px; padding: 1px 4px; margin-top: 3px; display: inline-block;">⛔ Excluded</div>' : '';

                const comp = c.completeness;
                let compHtml = '';
                if (comp.isExcluded) {
                    compHtml = '<span style="background: #f1f5f9; color: #64748b; font-size: 11px; padding: 2px 6px; border-radius: 4px; font-weight: 600;">Excluded</span>';
                } else if (comp.missingCount === 0) {
                    compHtml = '<span style="background: #dcfce7; color: #15803d; font-size: 11px; padding: 2px 8px; border-radius: 999px; font-weight: 700;">✓ ครบ 100%</span>';
                } else {
                    const compColor = comp.pct >= 80 ? '#d97706' : '#dc2626';
                    compHtml = `
                        <div style="cursor: pointer;" onclick="openFillBlanksModal('${c.studyId}')" title="คลิกเพื่อเติมช่องว่าง (${comp.missingCount} ช่อง)">
                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; margin-bottom: 2px;">
                                <span style="font-weight: 700; color: ${compColor};">${comp.pct}%</span>
                                <span style="font-size: 10px; color: #b91c1c; font-weight: 600;">ขาด ${comp.missingCount}</span>
                            </div>
                            <div style="height: 5px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
                                <div style="width: ${comp.pct}%; background: ${compColor}; height: 100%;"></div>
                            </div>
                        </div>
                    `;
                }

                rowsHtml += `
                    <tr class="admin-case-row" data-id="${c.studyId}">
                        <td style="text-align: center; font-weight: 700; color: #1e40af;">
                            <div>${c.displayId}</div>
                            ${ineligBadge}
                        </td>
                        <td>
                            <div><b>HN:</b> ${c.hn}</div>
                            <div style="font-size: 11.5px; color: #64748b;"><b>Ref:</b> ${c.referId}</div>
                        </td>
                        <td style="text-align: center;">${ageStr} / ${sexStr}</td>
                        <td style="text-align: center;">${esiBadge}</td>
                        <td>${condHtml}</td>
                        <td style="text-align: center;">${transferHtml}</td>
                        <td style="text-align: center; font-size: 12.5px;">${rtsHtml}</td>
                        <td style="text-align: center;">${outcomeHtml}</td>
                        <td style="text-align: center;">${compHtml}</td>
                        <td style="text-align: center;">
                            <div style="display: flex; gap: 4px; justify-content: center; flex-wrap: wrap;">
                                <button type="button" class="btn btn-outline" style="padding: 3px 7px; font-size: 11.5px; color: #d97706; border-color: #fcd34d; font-weight: 600;" onclick="openFillBlanksModal('${c.studyId}')" title="เปิดหน้าต่างเติมช่องว่างที่ยังไม่ได้กรอก">📝 เติมช่องว่าง</button>
                                <button type="button" class="btn btn-outline" style="padding: 3px 7px; font-size: 11.5px;" onclick="adminViewCase('${c.studyId}')" title="เปิดดูหรือแก้ไขเคสนี้">✏️ ดู/แก้ไข</button>
                                <button type="button" class="btn btn-outline" style="padding: 3px 7px; font-size: 11.5px; color: #1e40af; border-color: #93c5fd;" onclick="adminExportPDF('${c.studyId}')" title="ส่งออกรายงาน PDF">📄 PDF</button>
                                <button type="button" class="btn btn-outline" style="padding: 3px 7px; font-size: 11.5px; color: #b91c1c; border-color: #fca5a5;" onclick="adminDeleteCase('${c.studyId}')" title="ลบเคสนี้">🗑️ ลบ</button>
                            </div>
                        </td>
                    </tr>
                `;
            });
            tbody.innerHTML = rowsHtml;
        }

        // Update Sort Indicators on Table Headers
        updateAdminSortIndicators();

        // Update Overview Stat Cards
        const statTotal = document.getElementById('stat-total-patients');
        if (statTotal) statTotal.textContent = totalPatients;

        const statMean = document.getElementById('stat-mean-time');
        const statDetail = document.getElementById('stat-time-detail');
        if (statMean) {
            const avg = transferTimeCount > 0 ? (totalTransferMinutes / transferTimeCount).toFixed(1) : '0';
            statMean.innerHTML = avg + ' <span style="font-size: 14px; font-weight: 500;">นาที</span>';
        }
        if (statDetail) statDetail.textContent = 'คำนวณจาก ' + transferTimeCount + ' เคส';

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
        if (statSurvDetail) statSurvDetail.textContent = 'รอดชีวิต ' + survivalCount + ' / ประเมิน ' + mortalityAssessedCount + ' เคส';

        const statDeterCount = document.getElementById('stat-deter-count');
        const statDeterPct = document.getElementById('stat-deter-pct');
        const totalDeterAll = filtered.filter(c => c.isDeteriorated).length;
        if (statDeterCount) statDeterCount.textContent = totalDeterAll;
        if (statDeterPct) {
            const dpct = totalPatients > 0 ? ((totalDeterAll / totalPatients) * 100).toFixed(1) : '0';
            statDeterPct.textContent = dpct + '% เกิด AE หรือสรีรวิทยาแย่ลง';
        }

        const statCompleteness = document.getElementById('stat-data-completeness');
        const statMissingDetail = document.getElementById('stat-missing-cases-detail');
        if (statCompleteness) statCompleteness.textContent = overallCompletenessPct + '%';
        if (statMissingDetail) statMissingDetail.textContent = totalAuditMissing + ' ช่องว่างในระบบ (' + filtered.length + ' เคส)';

        const navMissingBadge = document.getElementById('admin-nav-missing-badge');
        if (navMissingBadge) navMissingBadge.textContent = totalAuditMissing;

        // Render Overview Donut Charts
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

        // =====================================================================
        // TAB 2: PRIMARY OBJECTIVE (Definitive Treatment Benchmarks)
        // =====================================================================
        const stemiEvalCases = filtered.filter(c => c.isStemi && (c.data.f4_eval_pci || c.data.f4_pci_d2b_min));
        const stemiAchieved = stemiEvalCases.filter(c => c.data.f4_eval_pci === 'achieved' || (parseFloat(c.data.f4_pci_d2b_min) > 0 && parseFloat(c.data.f4_pci_d2b_min) <= 180));
        const stemiD2BTimes = stemiEvalCases.map(c => parseFloat(c.data.f4_pci_d2b_min)).filter(t => !isNaN(t) && t > 0);

        const strokeEvalCases = filtered.filter(c => c.isStroke && (c.data.f4_eval_stroke || c.data.f4_stroke_o2n_min));
        const strokeAchieved = strokeEvalCases.filter(c => c.data.f4_eval_stroke === 'achieved' || (parseFloat(c.data.f4_stroke_o2n_min) > 0 && parseFloat(c.data.f4_stroke_o2n_min) <= 270));
        const strokeO2NTimes = strokeEvalCases.map(c => parseFloat(c.data.f4_stroke_o2n_min)).filter(t => !isNaN(t) && t > 0);

        const traumaEvalCases = filtered.filter(c => c.isTrauma && (c.data.f4_eval_trauma || c.data.f4_trauma_d2or_min || c.data.f4_trauma_d2ct_min));
        const traumaAchieved = traumaEvalCases.filter(c => c.data.f4_eval_trauma === 'achieved' || (parseFloat(c.data.f4_trauma_d2or_min) > 0 && parseFloat(c.data.f4_trauma_d2or_min) <= 180) || (parseFloat(c.data.f4_trauma_d2ct_min) > 0 && parseFloat(c.data.f4_trauma_d2ct_min) <= 150));
        const traumaORTimes = traumaEvalCases.map(c => parseFloat(c.data.f4_trauma_d2or_min)).filter(t => !isNaN(t) && t > 0);
        const traumaCTTimes = traumaEvalCases.map(c => parseFloat(c.data.f4_trauma_d2ct_min)).filter(t => !isNaN(t) && t > 0);

        const totalBenchmarkEval = stemiEvalCases.length + strokeEvalCases.length + traumaEvalCases.length;
        const totalBenchmarkAchieved = stemiAchieved.length + strokeAchieved.length + traumaAchieved.length;
        const overallAchievePct = totalBenchmarkEval > 0 ? (totalBenchmarkAchieved / totalBenchmarkEval) * 100 : 0;

        // Update Primary Tab Top Cards
        const primRateEl = document.getElementById('prim-overall-rate');
        const primDetailEl = document.getElementById('prim-overall-detail');
        if (primRateEl) primRateEl.textContent = overallAchievePct.toFixed(1) + '%';
        if (primDetailEl) primDetailEl.textContent = `${totalBenchmarkAchieved} / ${totalBenchmarkEval} เคสที่ได้รับการรักษา`;

        const primCardCombPct = document.getElementById('prim-card-combined-pct');
        const primCardCombSub = document.getElementById('prim-card-combined-sub');
        if (primCardCombPct) primCardCombPct.textContent = overallAchievePct.toFixed(1) + '%';
        if (primCardCombSub) primCardCombSub.textContent = `บรรลุ ${totalBenchmarkAchieved} จาก ${totalBenchmarkEval} เคส`;

        const stemiPct = stemiEvalCases.length > 0 ? (stemiAchieved.length / stemiEvalCases.length) * 100 : 0;
        const stemiMeanD2B = calcMean(stemiD2BTimes);
        const primCardStemiPct = document.getElementById('prim-card-stemi-pct');
        const primCardStemiMean = document.getElementById('prim-card-stemi-mean');
        if (primCardStemiPct) primCardStemiPct.textContent = `${stemiPct.toFixed(1)}% (${stemiAchieved.length}/${stemiEvalCases.length})`;
        if (primCardStemiMean) primCardStemiMean.textContent = `เวลาเฉลี่ย: ${stemiMeanD2B > 0 ? stemiMeanD2B.toFixed(0) : '--'} น. (เกณฑ์ ≤ 180 น.)`;

        const strokePct = strokeEvalCases.length > 0 ? (strokeAchieved.length / strokeEvalCases.length) * 100 : 0;
        const strokeMeanO2N = calcMean(strokeO2NTimes);
        const primCardStrokePct = document.getElementById('prim-card-stroke-pct');
        const primCardStrokeMean = document.getElementById('prim-card-stroke-mean');
        if (primCardStrokePct) primCardStrokePct.textContent = `${strokePct.toFixed(1)}% (${strokeAchieved.length}/${strokeEvalCases.length})`;
        if (primCardStrokeMean) primCardStrokeMean.textContent = `เวลาเฉลี่ย: ${strokeMeanO2N > 0 ? strokeMeanO2N.toFixed(0) : '--'} น. (เกณฑ์ ≤ 4.5 ชม.)`;

        const traumaPct = traumaEvalCases.length > 0 ? (traumaAchieved.length / traumaEvalCases.length) * 100 : 0;
        const traumaMeanOR = calcMean(traumaORTimes);
        const traumaMeanCT = calcMean(traumaCTTimes);
        const primCardTraumaPct = document.getElementById('prim-card-trauma-pct');
        const primCardTraumaMean = document.getElementById('prim-card-trauma-mean');
        if (primCardTraumaPct) primCardTraumaPct.textContent = `${traumaPct.toFixed(1)}% (${traumaAchieved.length}/${traumaEvalCases.length})`;
        if (primCardTraumaMean) primCardTraumaMean.textContent = `OR: ${traumaMeanOR > 0 ? traumaMeanOR.toFixed(0) + ' น.' : '--'} | CT: ${traumaMeanCT > 0 ? traumaMeanCT.toFixed(0) + ' น.' : '--'}`;

        // Render Chart 1: Achievement Stacked Bars
        const primChartBars = document.getElementById('prim-chart-bars');
        if (primChartBars) {
            const items = [
                { title: 'รวมทุกกลุ่มโรค (All Definitive Benchmarks)', evalCount: totalBenchmarkEval, achCount: totalBenchmarkAchieved, color: '#16a34a' },
                { title: 'STEMI: Door-to-Balloon (Primary PCI ≤ 180 น.)', evalCount: stemiEvalCases.length, achCount: stemiAchieved.length, color: '#dc2626' },
                { title: 'Stroke: Onset-to-Needle (IV rtPA ≤ 4.5 ชม.)', evalCount: strokeEvalCases.length, achCount: strokeAchieved.length, color: '#d97706' },
                { title: 'Severe Trauma: Emergent OR / CT Completion', evalCount: traumaEvalCases.length, achCount: traumaAchieved.length, color: '#7c3aed' }
            ];
            let barsHtml = '';
            items.forEach(it => {
                const achRate = it.evalCount > 0 ? (it.achCount / it.evalCount) * 100 : 0;
                const missRate = it.evalCount > 0 ? 100 - achRate : 0;
                barsHtml += `
                    <div>
                        <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:3px;">
                            <span style="font-weight:600; color:#1e293b;">${it.title}</span>
                            <span><b>${achRate.toFixed(1)}%</b> บรรลุเกณฑ์ (${it.achCount}/${it.evalCount} เคส)</span>
                        </div>
                        <div style="height:14px; background:#fee2e2; border-radius:999px; overflow:hidden; display:flex;">
                            <div style="width:${achRate}%; background:${it.color}; height:100%; transition:width 0.4s ease;" title="บรรลุเกณฑ์: ${achRate.toFixed(1)}%"></div>
                            <div style="width:${missRate}%; background:#ef4444; height:100%; opacity:0.85;" title="หลุดเกณฑ์: ${missRate.toFixed(1)}%"></div>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:10.5px; color:#64748b; margin-top:2px;">
                            <span>✓ บรรลุเกณฑ์ ${achRate.toFixed(0)}%</span>
                            <span>✕ หลุดเกณฑ์ ${missRate.toFixed(0)}%</span>
                        </div>
                    </div>
                `;
            });
            primChartBars.innerHTML = barsHtml;
        }

        // Render Chart 2: Actual Mean vs Target Limits
        const primChartDurations = document.getElementById('prim-chart-durations');
        if (primChartDurations) {
            const timeBenchmarks = [
                { name: 'STEMI: Door-to-Balloon (PCI)', actual: stemiMeanD2B, target: 180, maxScale: 300, unit: 'นาที' },
                { name: 'Stroke: Onset-to-Needle (rtPA)', actual: strokeMeanO2N, target: 270, maxScale: 400, unit: 'นาที' },
                { name: 'Severe Trauma: Door-to-OR', actual: traumaMeanOR, target: 180, maxScale: 300, unit: 'นาที' },
                { name: 'Severe Trauma: Door-to-CT', actual: traumaMeanCT, target: 150, maxScale: 250, unit: 'นาที' }
            ];
            let durHtml = '';
            timeBenchmarks.forEach(tb => {
                const actPct = tb.actual > 0 ? Math.min((tb.actual / tb.maxScale) * 100, 100) : 0;
                const tgtPct = (tb.target / tb.maxScale) * 100;
                const isBreach = tb.actual > tb.target;
                const color = isBreach ? '#dc2626' : '#16a34a';

                durHtml += `
                    <div>
                        <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:2px;">
                            <span style="font-weight:600; color:#1e293b;">${tb.name}</span>
                            <span style="color:${color}; font-weight:700;">เฉลี่ย ${tb.actual > 0 ? tb.actual.toFixed(0) : '--'} ${tb.unit} <span style="font-size:11px; font-weight:normal; color:#64748b;">(เกณฑ์ ≤ ${tb.target} ${tb.unit})</span></span>
                        </div>
                        <div style="height:12px; background:#f1f5f9; border-radius:999px; overflow:hidden; position:relative;">
                            <div style="width:${actPct}%; background:${color}; height:100%; border-radius:999px; transition:width 0.4s ease;"></div>
                            <div style="position:absolute; left:${tgtPct}%; top:0; bottom:0; width:2px; background:#0f172a; z-index:2;" title="เส้นเกณฑ์เป้าหมาย ${tb.target} ${tb.unit}"></div>
                        </div>
                    </div>
                `;
            });
            primChartDurations.innerHTML = durHtml;
        }

        // Render Table: Primary Benchmarks Summary
        const primTableBody = document.getElementById('prim-table-body');
        if (primTableBody) {
            const tableRows = [
                { name: 'STEMI Primary PCI (Door-to-Balloon)', bench: '≤ 180 นาที (Remote Primary PCI)', n: stemiEvalCases.length, ach: stemiAchieved.length, arr: stemiD2BTimes },
                { name: 'Stroke IV rtPA (Onset-to-Needle)', bench: '≤ 270 นาที (4.5 ชั่วโมง)', n: strokeEvalCases.length, ach: strokeAchieved.length, arr: strokeO2NTimes },
                { name: 'Trauma Emergent OR (Door-to-OR)', bench: '≤ 180 นาที (Damage Control OR)', n: traumaEvalCases.length, ach: traumaAchieved.length, arr: traumaORTimes },
                { name: 'Trauma CT Scan (Door-to-CT)', bench: '≤ 150 นาที (CT Completion)', n: traumaEvalCases.length, ach: traumaAchieved.length, arr: traumaCTTimes },
                { name: 'สรุปรวมทุกหัตถการรักษาจำเพาะ (Combined)', bench: 'บรรลุตามเกณฑ์ของแต่ละโรค', n: totalBenchmarkEval, ach: totalBenchmarkAchieved, arr: [] }
            ];
            let tHtml = '';
            tableRows.forEach(tr => {
                const achPct = tr.n > 0 ? ((tr.ach / tr.n) * 100).toFixed(1) + '%' : '-';
                const missN = tr.n - tr.ach;
                const missPct = tr.n > 0 ? ((missN / tr.n) * 100).toFixed(1) + '%' : '-';
                const meanStr = tr.arr.length > 0 ? `${calcMean(tr.arr).toFixed(1)} ± ${calcSD(tr.arr).toFixed(1)} น.` : '-';
                const medStr = tr.arr.length > 0 ? `${calcMedian(tr.arr).toFixed(0)} น. ${calcIQRStr(tr.arr)}` : '-';

                tHtml += `
                    <tr>
                        <td style="font-weight:600; color:#1e293b;">${tr.name}</td>
                        <td style="text-align:center; color:#475569;">${tr.bench}</td>
                        <td style="text-align:center; font-weight:700;">${tr.n}</td>
                        <td style="text-align:center; color:#16a34a; font-weight:700;">${tr.ach} (${achPct})</td>
                        <td style="text-align:center; color:#dc2626; font-weight:700;">${missN} (${missPct})</td>
                        <td style="text-align:center;">${meanStr}</td>
                        <td style="text-align:center;">${medStr}</td>
                    </tr>
                `;
            });
            primTableBody.innerHTML = tHtml;
        }

        // =====================================================================
        // TAB 3: SECONDARY OBJECTIVE 01 (Micro-timelines & Breaches)
        // =====================================================================
        const arrT01 = filtered.map(c => parseFloat(c.data.f2_t0_1_min)).filter(t => !isNaN(t) && t > 0);
        const arrT12 = filtered.map(c => parseFloat(c.data.f2_t2_min)).filter(t => !isNaN(t) && t > 0);
        const arrT23 = filtered.map(c => parseFloat(c.data.f2_t3_min)).filter(t => !isNaN(t) && t > 0);
        const arrT34 = filtered.map(c => parseFloat(c.data.f2_t4_min)).filter(t => !isNaN(t) && t > 0);
        const arrT45 = filtered.map(c => parseFloat(c.data.f2_t5_min)).filter(t => !isNaN(t) && t > 0);
        const arrTotal = filtered.map(c => c.transferMin).filter(t => !isNaN(t) && t > 0);

        const m01 = calcMean(arrT01);
        const m12 = calcMean(arrT12);
        const m23 = calcMean(arrT23);
        const m34 = calcMean(arrT34);
        const m45 = calcMean(arrT45);
        const mTotal = calcMean(arrTotal);

        // Breach thresholds
        const b01 = arrT01.filter(t => t > 60).length;
        const b12 = arrT12.filter(t => t > 25).length;
        const b23 = arrT23.filter(t => t > 30).length;
        const b34 = arrT34.filter(t => t > 45).length;
        const b45 = arrT45.filter(t => t > 60).length;
        const bTotal = arrTotal.filter(t => t > 180).length;

        const sec1MeanTotalEl = document.getElementById('sec1-mean-total');
        const sec1BreachBadgeEl = document.getElementById('sec1-total-breach-badge');
        if (sec1MeanTotalEl) sec1MeanTotalEl.innerHTML = `${mTotal.toFixed(0)} <span style="font-size: 14px; font-weight: 500;">นาที</span>`;
        if (sec1BreachBadgeEl) {
            const bPct = arrTotal.length > 0 ? ((bTotal / arrTotal.length) * 100).toFixed(1) : '0';
            sec1BreachBadgeEl.textContent = `ล่าช้าเกินเกณฑ์ ${bPct}% (${bTotal}/${arrTotal.length} เคส)`;
        }

        // Bottleneck identification
        const segments = [
            { id: 'T0-T1', name: 'ER เกาะลันตา (Pre-departure)', mean: m01, bench: 60, breaches: b01, arr: arrT01, color: '#3b82f6' },
            { id: 'T1-T2', name: 'รถวิ่งเกาะ ➔ ท่าแพคลองหมาก', mean: m12, bench: 25, breaches: b12, arr: arrT12, color: '#06b6d4' },
            { id: 'T2-T3', name: 'รอขึ้นแพขนานยนต์ (Ferry Wait)', mean: m23, bench: 30, breaches: b23, arr: arrT23, color: '#f59e0b' },
            { id: 'T3-T4', name: 'ข้ามฟากทางทะเล (Sea Crossing)', mean: m34, bench: 45, breaches: b34, arr: arrT34, color: '#8b5cf6' },
            { id: 'T4-T5', name: 'รถวิ่งแผ่นดินใหญ่ ➔ รพ.กระบี่', mean: m45, bench: 60, breaches: b45, arr: arrT45, color: '#10b981' }
        ];

        let maxMeanSeg = segments[0];
        segments.forEach(s => { if (s.mean > maxMeanSeg.mean) maxMeanSeg = s; });

        const bottleneckBadge = document.getElementById('sec1-bottleneck-badge');
        if (bottleneckBadge) {
            const share = mTotal > 0 ? ((maxMeanSeg.mean / mTotal) * 100).toFixed(0) : '0';
            bottleneckBadge.textContent = `⚠️ จุดคอขวดหลัก: ${maxMeanSeg.name} (เฉลี่ย ${maxMeanSeg.mean.toFixed(0)} นาที, ${share}% ของเวลารวม)`;
        }

        // Render Stacked Horizontal Continuum Bar
        const stackedBarEl = document.getElementById('sec1-stacked-bar-container');
        const stackedLegendEl = document.getElementById('sec1-stacked-legend');
        if (stackedBarEl && stackedLegendEl) {
            const sumSegs = m01 + m12 + m23 + m34 + m45;
            let barSegmentsHtml = '';
            let legendHtml = '';
            segments.forEach(s => {
                const segPct = sumSegs > 0 ? (s.mean / sumSegs) * 100 : 20;
                barSegmentsHtml += `
                    <div style="width:${segPct}%; background:${s.color}; height:100%; display:flex; align-items:center; justify-content:center; color:#ffffff; font-weight:700; font-size:11px; overflow:hidden; white-space:nowrap;" title="${s.name}: ${s.mean.toFixed(0)} นาที (${segPct.toFixed(0)}%)">
                        ${s.mean > 0 ? s.mean.toFixed(0) + 'น.' : ''}
                    </div>
                `;
                legendHtml += `
                    <div style="display:flex; align-items:center; gap:6px;">
                        <span style="width:10px; height:10px; border-radius:50%; background:${s.color};"></span>
                        <span><b>${s.id}:</b> ${s.name} (<b>${s.mean.toFixed(0)} น.</b> / ${segPct.toFixed(0)}%)</span>
                    </div>
                `;
            });
            stackedBarEl.innerHTML = barSegmentsHtml;
            stackedLegendEl.innerHTML = legendHtml;
        }

        // Render Breach Bars
        const sec1BreachBarsEl = document.getElementById('sec1-breach-bars');
        if (sec1BreachBarsEl) {
            let bBarsHtml = '';
            segments.concat([{ id: 'T_Total', name: 'เวลารวมทั้งระบบ (TTotal > 180 น.)', mean: mTotal, bench: 180, breaches: bTotal, arr: arrTotal, color: '#dc2626' }]).forEach(s => {
                const bPct = s.arr.length > 0 ? (s.breaches / s.arr.length) * 100 : 0;
                bBarsHtml += `
                    <div>
                        <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:2px;">
                            <span style="font-weight:600; color:#1e293b;">${s.id}: ${s.name}</span>
                            <span style="color:#b91c1c; font-weight:700;">หลุดเกณฑ์ ${bPct.toFixed(1)}% (${s.breaches}/${s.arr.length} เคส)</span>
                        </div>
                        <div style="height:10px; background:#f1f5f9; border-radius:999px; overflow:hidden;">
                            <div style="width:${bPct}%; background:${bPct > 30 ? '#dc2626' : '#f59e0b'}; height:100%; border-radius:999px; transition:width 0.4s ease;"></div>
                        </div>
                    </div>
                `;
            });
            sec1BreachBarsEl.innerHTML = bBarsHtml;
        }

        // Render Table: Micro-Interval Summary
        const sec1TableBody = document.getElementById('sec1-table-body');
        if (sec1TableBody) {
            let sHtml = '';
            segments.concat([{ id: 'T_Total', name: 'เวลารวมระบบส่งต่อ (T0 ➔ T5)', mean: mTotal, bench: '≤ 180 นาที', breaches: bTotal, arr: arrTotal, color: '#0f766e' }]).forEach(s => {
                const bPct = s.arr.length > 0 ? ((s.breaches / s.arr.length) * 100).toFixed(1) + '%' : '-';
                const meanStr = s.arr.length > 0 ? `${calcMean(s.arr).toFixed(1)} ± ${calcSD(s.arr).toFixed(1)} น.` : '-';
                const medStr = s.arr.length > 0 ? `${calcMedian(s.arr).toFixed(0)} น. ${calcIQRStr(s.arr)}` : '-';
                const benchStr = typeof s.bench === 'number' ? `≤ ${s.bench} นาที` : s.bench;

                sHtml += `
                    <tr>
                        <td style="font-weight:600; color:#1e293b;"><b>${s.id}:</b> ${s.name}</td>
                        <td style="text-align:center; color:#475569;">${benchStr}</td>
                        <td style="text-align:center;">${meanStr}</td>
                        <td style="text-align:center;">${medStr}</td>
                        <td style="text-align:center; color:#b91c1c; font-weight:700;">${s.breaches} (${bPct})</td>
                    </tr>
                `;
            });
            sec1TableBody.innerHTML = sHtml;
        }

        // =====================================================================
        // TAB 4: SECONDARY OBJECTIVE 02 (Bottlenecks & Delay Triggers)
        // =====================================================================
        const delayedCases = filtered.filter(c => !isNaN(c.transferMin) && c.transferMin > 180);
        const ontimeCases = filtered.filter(c => !isNaN(c.transferMin) && c.transferMin <= 180);

        const triggers = {
            patient: [
                { id: 'esi1', name: 'ผู้ป่วยวิกฤตระดับกู้ชีพ (ESI 1)', test: c => c.esi === '1' },
                { id: 'intub', name: 'ใส่ท่อช่วยหายใจ / ทางเดินหายใจวิกฤต', test: c => c.data.f2_ae_intub === '1' || (parseFloat(c.data.f1_gcs_total) <= 8 && c.data.f1_gcs_total !== '') },
                { id: 'shock', name: 'ภาวะช็อก / ใช้ยากระตุ้นหัวใจ', test: c => (parseFloat(c.data.f1_sbp) < 90 && c.data.f1_sbp !== '') || c.data.f2_ae_hypotension === '1' },
                { id: 'elderly', name: 'ผู้ป่วยสูงอายุ (Age > 60 ปี)', test: c => parseFloat(c.age) > 60 }
            ],
            operational: [
                { id: 'offhour', name: 'แพนอกเวลาปกติ (Off-Hour Ferry: 24:00–05:00 น.)', test: c => c.data.f2_ferry_operate === '1' || c.data.f3_ferry_shift === '1' },
                { id: 'night', name: 'เวรดึกห้องฉุกเฉินเกาะ (Night ED Shift: 00:00–08:00 น.)', test: c => c.data.f1_shift === 'night' || c.data.f3_ed_shift === 'night' },
                { id: 'queue', name: 'คิวรถติดสะสมหน้าท่าแพ (Pier Congestion)', test: c => c.data.f2_pier_congestion === '1' },
                { id: 'holiday', name: 'วันหยุดยาว / เทศกาลท่องเที่ยว (Holiday ≥ 3 วัน)', test: c => c.data.f3_holiday === '1' }
            ],
            maritime: [
                { id: 'monsoon', name: 'ฤดูมรสุมตะวันตกเฉียงใต้ (Monsoon: พ.ค.–ต.ค.)', test: c => c.data.f3_season === '0' },
                { id: 'lowtide', name: 'น้ำลงวิกฤต / สันดอนทราย (Tide < 1.0m / Sandbar)', test: c => c.data.f3_tide_extreme === '1' || c.data.f3_sandbar_risk === '1' || (parseFloat(c.data.f3_tide_height) < 1.0) },
                { id: 'roughsea', name: 'คลื่นลมแรงในทะเลอันดามัน (Waves > 2.0m)', test: c => c.data.f3_sea_state === '2' || (parseFloat(c.data.f3_wave_height) > 2.0) },
                { id: 'rain', name: 'พายุฝนตกหนักวิกฤต (Torrential Rain ≥ 10mm/hr)', test: c => c.data.f3_precipitation === '1' && (c.data.f3_torrential_rain === '1' || parseFloat(c.data.f3_rainfall_mm) >= 10.0) }
            ]
        };

        // Render Domain Horizontal Bar Charts
        let topTrigger = { name: '-', count: 0, pct: 0 };
        ['patient', 'operational', 'maritime'].forEach(domain => {
            const container = document.getElementById('sec2-bars-' + domain);
            if (!container) return;
            let dHtml = '';
            triggers[domain].forEach(trig => {
                const count = filtered.filter(trig.test).length;
                const pct = filtered.length > 0 ? (count / filtered.length) * 100 : 0;
                if (count > topTrigger.count) {
                    topTrigger = { name: trig.name, count: count, pct: pct };
                }

                dHtml += `
                    <div>
                        <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:2px;">
                            <span style="color:#1e293b; font-weight:500;">${trig.name}</span>
                            <span style="font-weight:700; color:#0f172a;">${pct.toFixed(0)}% <span style="font-size:10.5px; color:#64748b; font-weight:normal;">(${count} เคส)</span></span>
                        </div>
                        <div class="bar-horizontal-track">
                            <div class="bar-horizontal-fill" style="width:${pct}%; background:#3b82f6;"></div>
                        </div>
                    </div>
                `;
            });
            container.innerHTML = dHtml;
        });

        const topTrigNameEl = document.getElementById('sec2-top-trigger-name');
        const topTrigPctEl = document.getElementById('sec2-top-trigger-pct');
        if (topTrigNameEl) topTrigNameEl.textContent = topTrigger.count > 0 ? topTrigger.name : 'ยังไม่พบข้อมูล';
        if (topTrigPctEl) topTrigPctEl.textContent = topTrigger.count > 0 ? `พบใน ${topTrigger.pct.toFixed(1)}% (${topTrigger.count}/${filtered.length} เคส)` : 'พบใน 0% ของเคสทั้งหมด';

        // Render Contrast Analysis: Delayed vs On-Time
        const contrastContainer = document.getElementById('sec2-contrast-container');
        if (contrastContainer) {
            const allTrigs = [...triggers.patient, ...triggers.operational, ...triggers.maritime];
            let cHtml = '';
            allTrigs.slice(0, 6).forEach(trig => {
                const countDelay = delayedCases.filter(trig.test).length;
                const pctDelay = delayedCases.length > 0 ? (countDelay / delayedCases.length) * 100 : 0;
                const countOntime = ontimeCases.filter(trig.test).length;
                const pctOntime = ontimeCases.length > 0 ? (countOntime / ontimeCases.length) * 100 : 0;

                cHtml += `
                    <div style="border-bottom:1px solid #f1f5f9; padding-bottom:8px;">
                        <div style="font-size:12px; font-weight:600; color:#1e293b; margin-bottom:4px;">${trig.name}</div>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                            <div>
                                <div style="display:flex; justify-content:space-between; font-size:11px; color:#b91c1c;">
                                    <span>กลุ่มล่าช้า (> 3 ชม.)</span>
                                    <b>${pctDelay.toFixed(0)}% (${countDelay}/${delayedCases.length})</b>
                                </div>
                                <div class="bar-horizontal-track" style="height:8px;">
                                    <div class="bar-horizontal-fill" style="width:${pctDelay}%; background:#ef4444;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display:flex; justify-content:space-between; font-size:11px; color:#15803d;">
                                    <span>กลุ่มทันเวลา (≤ 3 ชม.)</span>
                                    <b>${pctOntime.toFixed(0)}% (${countOntime}/${ontimeCases.length})</b>
                                </div>
                                <div class="bar-horizontal-track" style="height:8px;">
                                    <div class="bar-horizontal-fill" style="width:${pctOntime}%; background:#22c55e;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            contrastContainer.innerHTML = cHtml;
        }

        // =====================================================================
        // TAB 5: SECONDARY OBJECTIVE 03 (Clinical Deterioration & Cohort RR)
        // =====================================================================
        const exposedCohort = filtered.filter(c => c.isExposed);
        const unexposedCohort = filtered.filter(c => !c.isExposed);

        const expTotalEl = document.getElementById('sec3-cohort-total');
        const expEl = document.getElementById('sec3-cohort-exposed');
        const expSubEl = document.getElementById('sec3-cohort-exposed-sub');
        const unexpEl = document.getElementById('sec3-cohort-unexposed');
        const unexpSubEl = document.getElementById('sec3-cohort-unexposed-sub');

        if (expTotalEl) expTotalEl.textContent = filtered.length;
        if (expEl) expEl.textContent = exposedCohort.length;
        if (expSubEl) {
            const pct = filtered.length > 0 ? ((exposedCohort.length / filtered.length) * 100).toFixed(1) : '0';
            expSubEl.textContent = `${pct}% • กลุ่มสัมผัสความล่าช้า/อุปสรรค`;
        }
        if (unexpEl) unexpEl.textContent = unexposedCohort.length;
        if (unexpSubEl) {
            const pct = filtered.length > 0 ? ((unexposedCohort.length / filtered.length) * 100).toFixed(1) : '0';
            unexpSubEl.textContent = `${pct}% • กลุ่มควบคุมส่งต่อทันเวลา`;
        }

        // Clinical Outcomes to evaluate
        const outcomes = [
            {
                name: 'ภาวะผู้ป่วยทรุดลงระหว่างส่งต่อ (In-Transit Clinical Deterioration)',
                desc: 'Composite: En-route CPR, ใส่ท่อช่วยหายใจฉุกเฉิน, ช็อก/ความดันตกวิกฤต',
                test: c => c.data.f2_composite_ae === '1' || c.data.f4_composite_deter === '1' || c.data.f2_ae_cpr === '1' || c.data.f2_ae_intub === '1'
            },
            {
                name: 'การเสียชีวิต ณ ห้องฉุกเฉิน รพ.กระบี่ (Mainland ED Death)',
                desc: 'MORT_ER_KBH = 1 (เสียชีวิตทันทีก่อนรับไว้รักษาในหอผู้ป่วย)',
                test: c => c.data.f4_mort_er === '1'
            },
            {
                name: 'การเสียชีวิตภายใน 24 ชม. แรกหลังรับไว้รักษา (24-Hour Mortality)',
                desc: 'MORT_24H_POST = 1 หรือ MORT_STATUS = 1 (เสียชีวิตภายใน 24 ชม.)',
                test: c => c.data.f4_mort_24h === '1' || c.data.f4_mort_status === '1'
            }
        ];

        let incidenceBarsHtml = '';
        let riskTableHtml = '';
        let takeawayStatements = [];

        outcomes.forEach(out => {
            const a = exposedCohort.filter(out.test).length;
            const b = exposedCohort.length - a;
            const c = unexposedCohort.filter(out.test).length;
            const d = unexposedCohort.length - c;

            const nExp = exposedCohort.length;
            const nUnexp = unexposedCohort.length;

            const iExp = nExp > 0 ? (a / nExp) * 100 : 0;
            const iUnexp = nUnexp > 0 ? (c / nUnexp) * 100 : 0;

            let rr = '-';
            let ciStr = '-';
            let arrStr = '-';

            if (nExp > 0 && nUnexp > 0) {
                const arr = iExp - iUnexp;
                arrStr = `${arr > 0 ? '+' : ''}${arr.toFixed(1)}%`;

                if (iUnexp === 0) {
                    if (iExp === 0) {
                        rr = '1.00';
                        ciStr = '[0.00 - 0.00]';
                    } else {
                        // Continuity correction (+0.5)
                        const rrAdj = ((a + 0.5) / (nExp + 0.5)) / ((0.5) / (nUnexp + 0.5));
                        rr = `${rrAdj.toFixed(2)}*`;
                        ciStr = '(Corrected)';
                    }
                } else {
                    const rrVal = (a / nExp) / (c / nUnexp);
                    rr = rrVal.toFixed(2);
                    const se = Math.sqrt((1 / (a || 0.5)) - (1 / nExp) + (1 / (c || 0.5)) - (1 / nUnexp));
                    const ciLow = Math.max(0.01, rrVal * Math.exp(-1.96 * se));
                    const ciHigh = rrVal * Math.exp(1.96 * se);
                    ciStr = `[${ciLow.toFixed(2)} - ${ciHigh.toFixed(2)}]`;
                }
            }

            // Side-by-side Incidence Bars
            incidenceBarsHtml += `
                <div>
                    <div style="font-size:12.5px; font-weight:700; color:#1e293b; margin-bottom:4px;">${out.name}</div>
                    <div style="font-size:11px; color:#64748b; margin-bottom:6px;">${out.desc}</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
                        <div>
                            <div style="display:flex; justify-content:space-between; font-size:11.5px; color:#b91c1c; margin-bottom:2px;">
                                <span>กลุ่ม Exposed (เสี่ยง/ล่าช้า)</span>
                                <b>${iExp.toFixed(1)}% (${a}/${nExp})</b>
                            </div>
                            <div class="bar-horizontal-track" style="height:12px; background:#fee2e2;">
                                <div class="bar-horizontal-fill" style="width:${iExp}%; background:#dc2626;"></div>
                            </div>
                        </div>
                        <div>
                            <div style="display:flex; justify-content:space-between; font-size:11.5px; color:#15803d; margin-bottom:2px;">
                                <span>กลุ่ม Unexposed (ทันเวลา)</span>
                                <b>${iUnexp.toFixed(1)}% (${c}/${nUnexp})</b>
                            </div>
                            <div class="bar-horizontal-track" style="height:12px; background:#dcfce7;">
                                <div class="bar-horizontal-fill" style="width:${iUnexp}%; background:#16a34a;"></div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // 2x2 Risk Table Row
            let interp = 'ความเสี่ยงเท่ากัน';
            if (rr !== '-' && parseFloat(rr) > 1.0) interp = `<span style="color:#b91c1c; font-weight:700;">เสี่ยงเพิ่มขึ้น ${rr} เท่า</span>`;
            else if (rr !== '-' && parseFloat(rr) < 1.0) interp = `<span style="color:#15803d; font-weight:700;">ความเสี่ยงลดลง</span>`;

            riskTableHtml += `
                <tr>
                    <td style="font-weight:600; color:#1e293b;">
                        <div>${out.name}</div>
                        <div style="font-size:11px; color:#64748b;">${out.desc}</div>
                    </td>
                    <td style="text-align:center; font-weight:700; color:#dc2626;">${a}/${nExp} (${iExp.toFixed(1)}%)</td>
                    <td style="text-align:center; font-weight:700; color:#16a34a;">${c}/${nUnexp} (${iUnexp.toFixed(1)}%)</td>
                    <td style="text-align:center; font-weight:700;">${rr} ${ciStr}</td>
                    <td style="text-align:center; font-weight:600;">${arrStr}</td>
                    <td style="text-align:center;">${interp}</td>
                </tr>
            `;

            if (rr !== '-' && parseFloat(rr) > 1.0) {
                takeawayStatements.push(`ผู้ป่วยในกลุ่มที่ส่งต่อล่าช้า/เผชิญอุปสรรค (Exposed Cohort) มีอุบัติการณ์เกิด <b>${out.name}</b> คิดเป็น ${iExp.toFixed(1)}% เทียบกับ ${iUnexp.toFixed(1)}% ในกลุ่มควบคุม (Relative Risk = ${rr})`);
            }
        });

        const incidenceBarsEl = document.getElementById('sec3-incidence-bars');
        if (incidenceBarsEl) incidenceBarsEl.innerHTML = incidenceBarsHtml;

        const riskTableEl = document.getElementById('sec3-risk-table-body');
        if (riskTableEl) riskTableEl.innerHTML = riskTableHtml;

        const takeawayTextEl = document.getElementById('sec3-takeaway-text');
        if (takeawayTextEl) {
            if (takeawayStatements.length > 0) {
                takeawayTextEl.innerHTML = takeawayStatements.map(s => `• ${s}`).join('<br><br>');
            } else {
                takeawayTextEl.innerHTML = `จากการวิเคราะห์เบื้องต้นในกลุ่มตัวอย่างปัจจุบัน (N=${filtered.length} เคส) ยังไม่พบความแตกต่างอย่างมีนัยสำคัญระหว่างกลุ่ม Exposed และ Unexposed หรือยังไม่มีรายงานการเกิด Adverse Clinical Outcomes`;
            }
        }

        // =====================================================================
        // TAB 6: CLINICAL DETERIORATION & ADVERSE EVENTS REPORT
        // =====================================================================
        const deterFiltered = filtered.filter(c => c.isDeteriorated);
        const stableFiltered = filtered.filter(c => !c.isDeteriorated);

        // 1. KPI Cards
        const deterTotalEl = document.getElementById('deter-kpi-total');
        const deterTotalSubEl = document.getElementById('deter-kpi-total-sub');
        const deterTransitEl = document.getElementById('deter-kpi-transit');
        const deterTransitSubEl = document.getElementById('deter-kpi-transit-sub');
        const deterPhysioEl = document.getElementById('deter-kpi-physio');
        const deterPhysioSubEl = document.getElementById('deter-kpi-physio-sub');
        const deterResuscEl = document.getElementById('deter-kpi-resusc');
        const deterResuscSubEl = document.getElementById('deter-kpi-resusc-sub');
        const deterMortEl = document.getElementById('deter-kpi-mort');
        const deterMortSubEl = document.getElementById('deter-kpi-mort-sub');

        const nAll = filtered.length;
        const nDeter = deterFiltered.length;
        const deterAllPct = nAll > 0 ? ((nDeter / nAll) * 100).toFixed(1) : '0';

        if (deterTotalEl) deterTotalEl.textContent = nDeter;
        if (deterTotalSubEl) deterTotalSubEl.textContent = `${deterAllPct}% • ทรุดระหว่างทางหรือสรีรวิทยาแย่ลง`;

        const nTransitAe = filtered.filter(c => c.hasTransitAE).length;
        const transitPct = nAll > 0 ? ((nTransitAe / nAll) * 100).toFixed(1) : '0';
        if (deterTransitEl) deterTransitEl.textContent = nTransitAe;
        if (deterTransitSubEl) deterTransitSubEl.textContent = `${transitPct}% • เกิดบนรถพยาบาลหรือบนแพ`;

        const nPhysio = filtered.filter(c => c.hasPhysioDeter).length;
        const physioPct = nAll > 0 ? ((nPhysio / nAll) * 100).toFixed(1) : '0';
        if (deterPhysioEl) deterPhysioEl.textContent = nPhysio;
        if (deterPhysioSubEl) deterPhysioSubEl.textContent = `${physioPct}% • ΔGCS ≤ -2, ΔMAP ช็อก, ΔKillip, ΔRTS`;

        const nResusc = filtered.filter(c => c.hasCpr || c.hasIntub).length;
        const resuscPct = nAll > 0 ? ((nResusc / nAll) * 100).toFixed(1) : '0';
        if (deterResuscEl) deterResuscEl.textContent = nResusc;
        if (deterResuscSubEl) deterResuscSubEl.textContent = `${resuscPct}% • ปั๊มหัวใจหรือใส่ท่อช่วยหายใจด่วน`;

        const nMortDeter = deterFiltered.filter(c => c.data.f4_mort_24h === '1' || c.data.f4_mort_status === '1' || c.data.f4_mort_er === '1').length;
        const mortDeterPct = nDeter > 0 ? ((nMortDeter / nDeter) * 100).toFixed(1) : '0';
        if (deterMortEl) deterMortEl.textContent = nMortDeter;
        if (deterMortSubEl) deterMortSubEl.textContent = `${mortDeterPct}% • เสียชีวิตในกลุ่มผู้ป่วยทรุดหนัก`;

        // 2. In-Transit Adverse Events Breakdown
        const transitItems = [
            { name: 'ภาวะหัวใจหยุดเต้นระหว่างทาง (En-route CPR)', test: c => c.hasCpr, color: '#dc2626' },
            { name: 'ใส่ท่อช่วยหายใจฉุกเฉิน (Emergency Intubation)', test: c => c.hasIntub, color: '#ea580c' },
            { name: 'ช็อก / เริ่มหรือเพิ่มขนาดยากระตุ้นความดัน (Inotropes Escalation)', test: c => c.hasInotropes, color: '#d97706' },
            { name: 'ท่อช่วยหายใจเลื่อนหลุด (ETT Dislodgement)', test: c => c.hasDislodge, color: '#9333ea' },
            { name: 'เสียชีวิตระหว่างการส่งต่อ (In-Transit Death)', test: c => c.hasTransitDeath, color: '#0f172a' }
        ];

        let transitHtml = '';
        transitItems.forEach(item => {
            const count = filtered.filter(item.test).length;
            const pct = nAll > 0 ? ((count / nAll) * 100).toFixed(1) : '0';
            const expCount = exposedCohort.filter(item.test).length;
            const unexpCount = unexposedCohort.filter(item.test).length;
            transitHtml += `
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:3px;">
                        <span style="font-weight:600; color:#1e293b;">${item.name}</span>
                        <span style="font-weight:700; color:${item.color};">${count} เคส <span style="font-weight:normal; color:#64748b; font-size:11px;">(${pct}%) • Exp: ${expCount} | Ctrl: ${unexpCount}</span></span>
                    </div>
                    <div class="bar-horizontal-track" style="height:10px; background:#f1f5f9;">
                        <div class="bar-horizontal-fill" style="width:${pct}%; background:${item.color};"></div>
                    </div>
                </div>
            `;
        });
        const transitBreakdownEl = document.getElementById('deter-breakdown-transit');
        if (transitBreakdownEl) transitBreakdownEl.innerHTML = transitHtml;

        // 3. Physiological Parameters Breakdown
        const physioItems = [
            { name: 'ระดับความรู้สึกตัวลดลงวิกฤต (ΔGCS ≤ -2 คะแนน)', test: c => c.hasGcsDeter, color: '#dc2626', denom: nAll },
            { name: 'ภาวะความดันตก / ช็อก (ΔMAP < 0 & MAP < 65 mmHg หรือ SBP < 90)', test: c => c.hasMapDeter, color: '#ea580c', denom: nAll },
            { name: 'ภาวะอุณหภูมิกายต่ำวิกฤต (ΔBT / Hypothermia < 35.0 °C)', test: c => c.hasHypo, color: '#2563eb', denom: nAll },
            { name: 'ภาวะหัวใจล้มเหลวทรุดหนัก (ΔKillip Class ≥ +1 หรือ IV ใน STEMI)', test: c => c.hasKillip, color: '#b91c1c', denom: filtered.filter(c => c.isStemi).length },
            { name: 'ดัชนีช็อกกล้ามเนื้อหัวใจทรุด (ΔMSI ≥ +0.15 ใน STEMI)', test: c => c.hasMsi, color: '#c026d3', denom: filtered.filter(c => c.isStemi).length },
            { name: 'ดัชนีความรุนแรงบาดเจ็บทรุดหนัก (ΔRTS ≤ -1.0 ใน Trauma)', test: c => c.hasRts, color: '#4f46e5', denom: filtered.filter(c => c.isTrauma).length }
        ];

        let physioHtml = '';
        physioItems.forEach(item => {
            const count = filtered.filter(item.test).length;
            const denom = item.denom || nAll;
            const pct = denom > 0 ? ((count / denom) * 100).toFixed(1) : '0';
            physioHtml += `
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; margin-bottom:3px;">
                        <span style="font-weight:600; color:#1e293b;">${item.name}</span>
                        <span style="font-weight:700; color:${item.color};">${count}/${denom} เคส <span style="font-weight:normal; color:#64748b; font-size:11px;">(${pct}%)</span></span>
                    </div>
                    <div class="bar-horizontal-track" style="height:10px; background:#f1f5f9;">
                        <div class="bar-horizontal-fill" style="width:${pct}%; background:${item.color};"></div>
                    </div>
                </div>
            `;
        });
        const physioBreakdownEl = document.getElementById('deter-breakdown-physio');
        if (physioBreakdownEl) physioBreakdownEl.innerHTML = physioHtml;

        // 4. Timeline Comparison (Deteriorated vs Stable)
        const calcDeterMean = (arr, fn) => {
            const vals = arr.map(fn).filter(v => v !== null && !isNaN(v) && v > 0);
            return vals.length > 0 ? (vals.reduce((s, v) => s + v, 0) / vals.length) : null;
        };

        const timelines = [
            { name: 'เวลาส่งต่อรวมทั้งสิ้น (T0 ➔ T5 Total Transfer)', getVal: c => c.transferMin, maxBench: 180 },
            { name: 'เวลาเตรียมส่ง ณ รพ.เกาะลันตา (T0 ➔ T1 DIDO)', getVal: c => c.t0ToT1, maxBench: 30 },
            { name: 'เวลารอขึ้นแพขนานยนต์ (T2 ➔ T3 Pier Waiting)', getVal: c => c.t2ToT3, maxBench: 10 },
            { name: 'เวลาแพข้ามฟากทางทะเล (T3 Ferry Crossing)', getVal: c => c.t3Dur, maxBench: 15 },
            { name: 'เวลาเริ่มหัตถการ ณ รพ.กระบี่ (T4 ➔ T5 Door-to-Intervention)', getVal: c => c.t4ToT5, maxBench: 45 }
        ];

        let timelineHtml = '';
        timelines.forEach(tl => {
            const mDeter = calcDeterMean(deterFiltered, tl.getVal);
            const mStable = calcDeterMean(stableFiltered, tl.getVal);
            const mDeterStr = mDeter !== null ? mDeter.toFixed(1) : '-';
            const mStableStr = mStable !== null ? mStable.toFixed(1) : '-';
            const diff = (mDeter !== null && mStable !== null) ? (mDeter - mStable) : null;
            const diffStr = diff !== null ? `${diff > 0 ? '+' : ''}${diff.toFixed(1)} นาที` : '-';
            const diffColor = diff !== null && diff > 0 ? '#b91c1c' : '#15803d';

            timelineHtml += `
                <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:6px; padding:10px 14px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="font-weight:700; color:#1e293b; font-size:12.5px;">${tl.name}</span>
                        <span style="font-weight:700; color:${diffColor}; font-size:12px;">ผลต่าง: ${diffStr}</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                        <div>
                            <div style="display:flex; justify-content:space-between; font-size:11.5px; color:#b91c1c; margin-bottom:2px;">
                                <span>กลุ่มทรุดลง (Deteriorated, N=${nDeter})</span>
                                <b>${mDeterStr} นาที</b>
                            </div>
                            <div class="bar-horizontal-track" style="height:10px; background:#fee2e2;">
                                <div class="bar-horizontal-fill" style="width:${Math.min(100, mDeter ? (mDeter / (tl.maxBench * 1.5)) * 100 : 0)}%; background:#dc2626;"></div>
                            </div>
                        </div>
                        <div>
                            <div style="display:flex; justify-content:space-between; font-size:11.5px; color:#15803d; margin-bottom:2px;">
                                <span>กลุ่มคงที่ (Stable, N=${stableFiltered.length})</span>
                                <b>${mStableStr} นาที</b>
                            </div>
                            <div class="bar-horizontal-track" style="height:10px; background:#dcfce7;">
                                <div class="bar-horizontal-fill" style="width:${Math.min(100, mStable ? (mStable / (tl.maxBench * 1.5)) * 100 : 0)}%; background:#16a34a;"></div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        const timelineCompEl = document.getElementById('deter-timeline-comparison');
        if (timelineCompEl) timelineCompEl.innerHTML = timelineHtml;

        // 5. Subgroups Matrix (Disease & Acuity/Cohort)
        const stemiAll = filtered.filter(c => c.isStemi);
        const strokeAll = filtered.filter(c => c.isStroke);
        const traumaAll = filtered.filter(c => c.isTrauma);
        const stemiDeter = stemiAll.filter(c => c.isDeteriorated).length;
        const strokeDeter = strokeAll.filter(c => c.isDeteriorated).length;
        const traumaDeter = traumaAll.filter(c => c.isDeteriorated).length;

        const diseaseMatrixEl = document.getElementById('deter-disease-matrix');
        if (diseaseMatrixEl) {
            diseaseMatrixEl.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 10px; background:#f8fafc; border-radius:4px; font-size:12.5px;">
                    <span style="font-weight:600; color:#1e293b;">🫀 STEMI / ACS:</span>
                    <b style="color:#dc2626;">${stemiDeter}/${stemiAll.length} (${stemiAll.length > 0 ? ((stemiDeter / stemiAll.length) * 100).toFixed(1) : '0'}%)</b>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 10px; background:#f8fafc; border-radius:4px; font-size:12.5px;">
                    <span style="font-weight:600; color:#1e293b;">🧠 Acute Stroke:</span>
                    <b style="color:#d97706;">${strokeDeter}/${strokeAll.length} (${strokeAll.length > 0 ? ((strokeDeter / strokeAll.length) * 100).toFixed(1) : '0'}%)</b>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 10px; background:#f8fafc; border-radius:4px; font-size:12.5px;">
                    <span style="font-weight:600; color:#1e293b;">🩹 Severe Trauma:</span>
                    <b style="color:#2563eb;">${traumaDeter}/${traumaAll.length} (${traumaAll.length > 0 ? ((traumaDeter / traumaAll.length) * 100).toFixed(1) : '0'}%)</b>
                </div>
            `;
        }

        const esi1All = filtered.filter(c => c.esi === '1');
        const esi2All = filtered.filter(c => c.esi === '2');
        const esi1Deter = esi1All.filter(c => c.isDeteriorated).length;
        const esi2Deter = esi2All.filter(c => c.isDeteriorated).length;
        const expDeter = exposedCohort.filter(c => c.isDeteriorated).length;
        const unexpDeter = unexposedCohort.filter(c => c.isDeteriorated).length;
        const expPct = exposedCohort.length > 0 ? ((expDeter / exposedCohort.length) * 100).toFixed(1) : '0';
        const unexpPct = unexposedCohort.length > 0 ? ((unexpDeter / unexposedCohort.length) * 100).toFixed(1) : '0';

        let cohortRRStr = '-';
        if (exposedCohort.length > 0 && unexposedCohort.length > 0) {
            const pExp = expDeter / exposedCohort.length;
            const pUnexp = unexpDeter / unexposedCohort.length;
            if (pUnexp > 0) cohortRRStr = (pExp / pUnexp).toFixed(2);
            else if (pExp > 0) cohortRRStr = 'High (Unexp=0%)';
            else cohortRRStr = '1.00';
        }

        const acuityMatrixEl = document.getElementById('deter-acuity-matrix');
        if (acuityMatrixEl) {
            acuityMatrixEl.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 10px; background:#f8fafc; border-radius:4px; font-size:12.5px;">
                    <span style="font-weight:600; color:#1e293b;">⚡ ESI 1 (Resuscitation):</span>
                    <b style="color:#dc2626;">${esi1Deter}/${esi1All.length} (${esi1All.length > 0 ? ((esi1Deter / esi1All.length) * 100).toFixed(1) : '0'}%)</b>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 10px; background:#f8fafc; border-radius:4px; font-size:12.5px;">
                    <span style="font-weight:600; color:#1e293b;">⚠️ ESI 2 (Emergent):</span>
                    <b style="color:#ea580c;">${esi2Deter}/${esi2All.length} (${esi2All.length > 0 ? ((esi2Deter / esi2All.length) * 100).toFixed(1) : '0'}%)</b>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 10px; background:#eff6ff; border-radius:4px; font-size:12.5px; border:1px solid #bfdbfe;">
                    <span style="font-weight:700; color:#1e40af;">⚖️ Exposed vs Unexposed (RR):</span>
                    <b style="color:#1e40af;">${expPct}% vs ${unexpPct}% (RR = ${cohortRRStr})</b>
                </div>
            `;
        }

        // 6. Detailed Audit Table
        const deterTableBadge = document.getElementById('deter-table-count-badge');
        if (deterTableBadge) deterTableBadge.textContent = `${deterFiltered.length} เคส`;

        const deterTbody = document.getElementById('deter-cases-tbody');
        if (deterTbody) {
            if (deterFiltered.length === 0) {
                deterTbody.innerHTML = '<tr><td colspan="8" style="text-align:center; padding:20px; color:#64748b; font-size:13px;">ไม่พบเคสที่เกิดภาวะทรุดลงตามเงื่อนไขตัวกรอง</td></tr>';
            } else {
                let dRowsHtml = '';
                deterFiltered.forEach(c => {
                    const disBadge = c.isStemi ? '<span style="background:#fee2e2; color:#991b1b; padding:2px 6px; border-radius:4px; font-weight:700; font-size:11px;">STEMI</span>'
                        : (c.isStroke ? '<span style="background:#fef3c7; color:#92400e; padding:2px 6px; border-radius:4px; font-weight:700; font-size:11px;">Stroke</span>'
                        : '<span style="background:#dbeafe; color:#1e40af; padding:2px 6px; border-radius:4px; font-weight:700; font-size:11px;">Trauma</span>');

                    const esiBadge = c.esi === '1' ? '<span style="background:#dc2626; color:#ffffff; padding:2px 6px; border-radius:4px; font-weight:700; font-size:11px;">ESI 1</span>'
                        : '<span style="background:#f97316; color:#ffffff; padding:2px 6px; border-radius:4px; font-weight:700; font-size:11px;">ESI 2</span>';

                    const cohortBadge = c.isExposed ? '<span style="background:#fef2f2; color:#b91c1c; border:1px solid #fecaca; padding:2px 6px; border-radius:4px; font-size:11px; font-weight:700;">Exposed</span>'
                        : '<span style="background:#f0fdf4; color:#15803d; border:1px solid #bbf7d0; padding:2px 6px; border-radius:4px; font-size:11px; font-weight:700;">Control</span>';

                    const transitBadges = [];
                    if (c.hasCpr) transitBadges.push('<span style="background:#fee2e2; color:#991b1b; padding:1px 5px; border-radius:3px; font-size:10.5px; font-weight:700;">CPR</span>');
                    if (c.hasIntub) transitBadges.push('<span style="background:#ffedd5; color:#9a3412; padding:1px 5px; border-radius:3px; font-size:10.5px; font-weight:600;">Intubation</span>');
                    if (c.hasInotropes) transitBadges.push('<span style="background:#fef3c7; color:#854d0e; padding:1px 5px; border-radius:3px; font-size:10.5px; font-weight:600;">Inotropes</span>');
                    if (c.hasTransitDeath) transitBadges.push('<span style="background:#0f172a; color:#ffffff; padding:1px 5px; border-radius:3px; font-size:10.5px; font-weight:700;">In-transit Death</span>');
                    const transitDisplay = transitBadges.length > 0 ? transitBadges.join(' ') : '<span style="color:#94a3b8; font-size:11px;">-</span>';

                    const physioBadges = [];
                    if (c.hasGcsDeter) physioBadges.push(`<span style="background:#fce7f3; color:#9d174d; padding:1px 5px; border-radius:3px; font-size:10.5px;">ΔGCS ${c.data.f4_delta_gcs || '≤-2'}</span>`);
                    if (c.hasMapDeter) physioBadges.push('<span style="background:#fee2e2; color:#b91c1c; padding:1px 5px; border-radius:3px; font-size:10.5px;">ΔMAP Shock</span>');
                    if (c.hasHypo) physioBadges.push('<span style="background:#e0e7ff; color:#3730a3; padding:1px 5px; border-radius:3px; font-size:10.5px;">Hypothermia</span>');
                    if (c.hasKillip) physioBadges.push('<span style="background:#fee2e2; color:#991b1b; padding:1px 5px; border-radius:3px; font-size:10.5px;">ΔKillip IV</span>');
                    if (c.hasMsi) physioBadges.push('<span style="background:#fae8ff; color:#86198f; padding:1px 5px; border-radius:3px; font-size:10.5px;">ΔMSI High</span>');
                    if (c.hasRts) physioBadges.push('<span style="background:#e0e7ff; color:#1e40af; padding:1px 5px; border-radius:3px; font-size:10.5px;">ΔRTS Drop</span>');
                    const physioDisplay = physioBadges.length > 0 ? physioBadges.join(' ') : '<span style="color:#94a3b8; font-size:11px;">-</span>';

                    const tMinStr = !isNaN(c.transferMin) && c.transferMin > 0 ? `${c.transferMin} นาที` : '-';
                    const isDelayed = c.transferMin > 180;
                    const timeDisplay = isDelayed ? `<b style="color:#b91c1c;">${tMinStr} ⚠️</b>` : `<span style="color:#15803d;">${tMinStr}</span>`;

                    let mortDisplay = '<span style="color:#15803d; font-weight:600;">รอดชีวิต</span>';
                    if (c.data.f4_mort_er === '1') mortDisplay = '<b style="color:#dc2626;">เสียชีวิต ณ ER</b>';
                    else if (c.data.f4_mort_24h === '1' || c.data.f4_mort_status === '1') mortDisplay = '<b style="color:#b91c1c;">เสียชีวิต 24 ชม.</b>';

                    dRowsHtml += `
                        <tr>
                            <td style="font-weight:700; color:#1e40af; text-align:center;">LANTA_${c.studyId}</td>
                            <td style="text-align:center;">${disBadge} ${esiBadge}</td>
                            <td style="text-align:center;">${cohortBadge}</td>
                            <td>${transitDisplay}</td>
                            <td>${physioDisplay}</td>
                            <td style="text-align:center;">${timeDisplay}</td>
                            <td style="text-align:center;">${mortDisplay}</td>
                            <td style="text-align:center;">
                                <button type="button" class="btn btn-outline" style="padding:2px 8px; font-size:11px;" onclick="adminViewCase('${c.studyId}')">🔍 ดูเคส</button>
                            </td>
                        </tr>
                    `;
                });
                deterTbody.innerHTML = dRowsHtml;
            }
        }

        // 7. Clinical Takeaway Box
        const deterTakeawayEl = document.getElementById('deter-takeaway-text');
        if (deterTakeawayEl) {
            const mDiffTotal = (calcDeterMean(deterFiltered, c => c.transferMin) || 0) - (calcDeterMean(stableFiltered, c => c.transferMin) || 0);
            const mDiffPier = (calcDeterMean(deterFiltered, c => c.t2ToT3) || 0) - (calcDeterMean(stableFiltered, c => c.t2ToT3) || 0);
            const mDiffFerry = (calcDeterMean(deterFiltered, c => c.t3Dur) || 0) - (calcDeterMean(stableFiltered, c => c.t3Dur) || 0);

            deterTakeawayEl.innerHTML = `
                • ในกลุ่มตัวอย่างปัจจุบัน (N=${nAll} เคส) พบผู้ป่วยที่เกิดภาวะทรุดลงระหว่างส่งต่อหรือสรีรวิทยาแย่ลงรวม <b>${nDeter} เคส (${deterAllPct}%)</b><br>
                • ผู้ป่วยในกลุ่ม Exposed มีอุบัติการณ์เกิดภาวะทรุดลงคิดเป็น <b>${expPct}%</b> เทียบกับ <b>${unexpPct}%</b> ในกลุ่ม Unexposed/Control <b>(Relative Risk = ${cohortRRStr})</b><br>
                • ผู้ป่วยที่เกิดภาวะทรุดลงมีเวลาส่งต่อเฉลี่ยยาวนานกว่ากลุ่มสัญญาณชีพคงที่ถึง <b>+${mDiffTotal.toFixed(1)} นาที</b> โดยพบความต่างสูงที่สุดในช่วงเวลารอขึ้นแพขนานยนต์ (+${mDiffPier.toFixed(1)} นาที) และช่วงแพข้ามฟาก (+${mDiffFerry.toFixed(1)} นาที)<br>
                • ผู้ป่วยวิกฤตระดับ <b>ESI 1</b> มีอัตราการทรุดลง (${esi1All.length > 0 ? ((esi1Deter / esi1All.length) * 100).toFixed(1) : '0'}%) สูงกว่ากลุ่ม ESI 2 อย่างมีนัยสำคัญ บ่งชี้ความจำเป็นเร่งด่วนในการพัฒนาระบบ <i>Maritime Fast-Track</i> และทีมบริบาลช่วยฟื้นคืนชีพระดับสูงบนเรือ/แพขนานยนต์
            `;
        }

        // =====================================================================
        // TAB 7: MISSING DATA & COMPLETENESS AUDIT
        // =====================================================================
        renderMissingDataAudit(allCases, filtered, missingByForm, expectedByForm, totalAuditMissing, overallCompletenessPct);
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
        renderAdminDashboard();
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

        localStorage.removeItem('online_crf_case_' + studyId);
        let index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
        index = index.filter(id => id !== studyId);
        localStorage.setItem('online_crf_case_index', JSON.stringify(index));

        const curActive = localStorage.getItem('online_crf_last_active_id');
        if (curActive === studyId) {
            if (index.length > 0) loadCase(index[0]);
            else createNewCase();
        }

        loadCaseIndex();
        renderAdminDashboard();
        alert('✓ ลบข้อมูลเคส LANTA_' + studyId + ' เรียบร้อยแล้ว');
    }

    // =========================================================================
    // MISSING DATA AUDIT & POPUP FILL BLANKS MODAL ENGINE
    // =========================================================================
    function renderMissingDataAudit(allCases, filtered, missingByForm, expectedByForm, totalAuditMissing, overallCompletenessPct) {
        // 1. Top Banner
        const rateEl = document.getElementById('audit-overall-rate');
        const detailEl = document.getElementById('audit-overall-detail');
        if (rateEl) rateEl.textContent = overallCompletenessPct + '%';
        if (detailEl) {
            detailEl.textContent = totalAuditMissing + ' ช่องว่าง จาก ' + filtered.length + ' เคส';
        }

        // 2. 4 Form KPI Cards
        for (let f = 1; f <= 4; f++) {
            const exp = expectedByForm[f] || 0;
            const mis = missingByForm[f] || 0;
            const filled = exp - mis;
            const pct = exp > 0 ? Math.round((filled / exp) * 100) : 100;

            const badgeEl = document.getElementById('audit-f' + f + '-badge');
            const pctEl = document.getElementById('audit-f' + f + '-pct');
            const subEl = document.getElementById('audit-f' + f + '-sub');

            if (badgeEl) badgeEl.textContent = mis + ' ช่อง';
            if (pctEl) pctEl.textContent = pct + '%';
            if (subEl) subEl.textContent = 'กรอกแล้ว ' + filled + '/' + exp + ' ตัวแปร';
        }

        // 3. Audit Cases Table
        const tbody = document.getElementById('audit-cases-tbody');
        if (!tbody) return;

        const incompleteOnly = document.getElementById('audit-filter-incomplete-only')?.checked ?? true;
        const auditCases = incompleteOnly ? filtered.filter(c => c.completeness && c.completeness.missingCount > 0) : filtered;

        if (auditCases.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 25px; color: #16a34a; font-size: 13.5px; font-weight: 600;">🎉 ยอดเยี่ยม! ไม่พบเคสที่มีข้อมูลตกหล่นตามเงื่อนไขตัวกรอง</td></tr>';
            return;
        }

        function renderChipsForForm(c, formNum) {
            if (c.completeness.isExcluded && formNum > 1) {
                return '<span style="color: #94a3b8; font-size: 11px; font-style: italic;">(Excluded)</span>';
            }
            const formInfo = c.completeness.byForm[formNum];
            const missingList = formInfo ? formInfo.missing : [];
            if (!missingList || missingList.length === 0) {
                return '<span style="color: #16a34a; font-size: 11px; font-weight: 700;">✓ ครบถ้วน</span>';
            }

            const maxVisible = 2;
            const visible = missingList.slice(0, maxVisible);
            const remainder = missingList.length - maxVisible;

            let html = '<div style="display: flex; flex-wrap: wrap; gap: 4px;">';
            visible.forEach(f => {
                html += `<span class="missing-chip" onclick="openFillBlanksModal('${c.studyId}', '${f.key}')" title="คลิกเพื่อเติม: ${f.label}">${f.label}</span>`;
            });
            if (remainder > 0) {
                html += `<span class="missing-chip" style="background: #e2e8f0; color: #334155;" onclick="openFillBlanksModal('${c.studyId}')" title="คลิกเพื่อดูช่องว่างทั้งหมด">+ อีก ${remainder} ช่อง</span>`;
            }
            html += '</div>';
            return html;
        }

        let rowsHtml = '';
        auditCases.forEach(c => {
            const comp = c.completeness;
            const disBadge = c.isStemi ? '<span style="background:#fee2e2; color:#991b1b; padding:2px 6px; border-radius:4px; font-weight:700; font-size:11px;">STEMI</span>'
                : (c.isStroke ? '<span style="background:#fef3c7; color:#92400e; padding:2px 6px; border-radius:4px; font-weight:700; font-size:11px;">Stroke</span>'
                : (c.isTrauma ? '<span style="background:#ede9fe; color:#5b21b6; padding:2px 6px; border-radius:4px; font-weight:700; font-size:11px;">Trauma</span>'
                : '<span style="color:#64748b; font-size:11px;">อื่นๆ</span>'));

            const compColor = comp.pct >= 80 ? '#d97706' : (comp.pct === 100 ? '#16a34a' : '#dc2626');
            const compHtml = `
                <div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px; font-weight:700; color:${compColor};">
                        <span>${comp.pct}%</span>
                        <span style="font-size:10px; color:#b91c1c;">ขาด ${comp.missingCount}</span>
                    </div>
                    <div style="height:5px; background:#e2e8f0; border-radius:999px; overflow:hidden;">
                        <div style="width:${comp.pct}%; background:${compColor}; height:100%;"></div>
                    </div>
                </div>
            `;

            rowsHtml += `
                <tr>
                    <td style="text-align: center; font-weight: 700; color: #1e40af;">
                        LANTA_${c.studyId}
                    </td>
                    <td>
                        <div><b>HN:</b> ${c.hn}</div>
                        <div style="font-size: 11px; color: #64748b;"><b>Ref:</b> ${c.referId}</div>
                    </td>
                    <td style="text-align: center;">${disBadge}</td>
                    <td>${renderChipsForForm(c, 1)}</td>
                    <td>${renderChipsForForm(c, 2)}</td>
                    <td>${renderChipsForForm(c, 3)}</td>
                    <td>${renderChipsForForm(c, 4)}</td>
                    <td style="text-align: center;">${compHtml}</td>
                    <td style="text-align: center;">
                        <button type="button" class="btn btn-warning" style="padding: 3px 8px; font-size: 11.5px; font-weight: 700; white-space: nowrap;" onclick="openFillBlanksModal('${c.studyId}')">
                            📝 เติมช่องว่าง
                        </button>
                    </td>
                </tr>
            `;
        });
        tbody.innerHTML = rowsHtml;
    }

    let currentBlanksStudyId = null;
    let currentBlanksShowAll = false;

    function openFillBlanksModal(studyId, focusKey = null) {
        currentBlanksStudyId = studyId;
        currentBlanksShowAll = false;

        const toggleBtn = document.getElementById('blanks-toggle-all-btn');
        if (toggleBtn) toggleBtn.innerHTML = '👁️ แสดงทุกช่อง';

        const feedbackEl = document.getElementById('blanks-save-feedback');
        if (feedbackEl) feedbackEl.style.display = 'none';

        renderBlanksModalBody(studyId, false, focusKey);

        const modalEl = document.getElementById('fill-blanks-modal');
        if (modalEl) modalEl.style.display = 'flex';
    }

    function toggleBlanksFilterAll() {
        if (!currentBlanksStudyId) return;
        currentBlanksShowAll = !currentBlanksShowAll;
        const toggleBtn = document.getElementById('blanks-toggle-all-btn');
        if (toggleBtn) {
            toggleBtn.innerHTML = currentBlanksShowAll ? '⚡ แสดงเฉพาะช่องว่าง' : '👁️ แสดงทุกช่อง';
        }
        renderBlanksModalBody(currentBlanksStudyId, currentBlanksShowAll);
    }

    function closeFillBlanksModal() {
        const modalEl = document.getElementById('fill-blanks-modal');
        if (modalEl) modalEl.style.display = 'none';
        currentBlanksStudyId = null;
    }

    function renderBlanksModalBody(studyId, showAll = false, focusKey = null) {
        const raw = localStorage.getItem('online_crf_case_' + studyId);
        if (!raw) return;
        const data = JSON.parse(raw);

        // Subtitle
        const subEl = document.getElementById('blanks-modal-subtitle');
        if (subEl) {
            const diseaseName = isCaseStemi(data) ? 'STEMI' : (isCaseStroke(data) ? 'Acute Stroke' : (isCaseTrauma(data) ? 'Severe Trauma' : 'ทั่วไป'));
            subEl.innerHTML = `ผู้ป่วย: <b>LANTA_${studyId}</b> | HN: <b>${data.f1_hn || '-'}</b> | Refer: <b>${data.f1_refer_id || '-'}</b> | กลุ่มโรค: <span style="background:rgba(255,255,255,0.25); padding:1px 6px; border-radius:4px; font-weight:700;">${diseaseName}</span>`;
        }

        // Completeness calculation
        const comp = getCaseCompleteness(data);
        const countText = document.getElementById('blanks-modal-count-text');
        const pctText = document.getElementById('blanks-modal-pct-text');
        const progressBar = document.getElementById('blanks-modal-progress-bar');

        if (countText) {
            countText.textContent = comp.missingCount === 0 ? '✓ ข้อมูลสมบูรณ์ครบถ้วน 100%' : `พบช่องว่างที่ยังไม่ได้บันทึก ${comp.missingCount} ช่อง`;
            countText.style.color = comp.missingCount === 0 ? '#15803d' : '#b45309';
        }
        if (pctText) pctText.textContent = `${comp.pct}% สมบูรณ์`;
        if (progressBar) {
            progressBar.style.width = comp.pct + '%';
            progressBar.style.background = comp.pct === 100 ? '#16a34a' : (comp.pct >= 80 ? '#f59e0b' : '#ef4444');
        }

        const bodyEl = document.getElementById('blanks-modal-body');
        if (!bodyEl) return;

        const isExcluded = (data.f1_eligible === 'excluded');
        const formNames = {
            1: 'Form 1: ข้อมูลแรกรับและคัดกรอง ณ รพ.เกาะลันตา',
            2: 'Form 2: ไทม์ไลน์และเหตุการณ์ระหว่างส่งต่อทางทะเลและบก',
            3: 'Form 3: สภาพอากาศ คลื่นลม และตารางน้ำขึ้นน้ำลง',
            4: 'Form 4: การรักษา ณ รพ.กระบี่ และผลลัพธ์การรอดชีวิต 24 ชม.'
        };
        const formBadges = {
            1: { color: '#b45309', bg: '#fef3c7' },
            2: { color: '#1e40af', bg: '#dbeafe' },
            3: { color: '#0e7490', bg: '#cffafe' },
            4: { color: '#6d28d9', bg: '#ede9fe' }
        };

        let formsHtml = '';
        let totalRenderedFields = 0;

        for (let f = 1; f <= 4; f++) {
            if (isExcluded && f > 1) continue;

            const fieldsForForm = CRF_AUDIT_FIELDS.filter(item => {
                if (item.form !== f) return false;
                if (isExcluded && (item.category !== ข้อมูลทั่วไปและผู้สกัด && item.category !== เกณฑ์การคัดกรองวิจัย)) return false;
                if (item.condition && !item.condition(data)) return false;
                if (!showAll && isFieldFilled(data, item.key) && focusKey !== item.key) return false;
                return true;
            });

            if (fieldsForForm.length === 0) continue;

            totalRenderedFields += fieldsForForm.length;
            const fb = formBadges[f];

            formsHtml += `
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; background: #f8fafc; border-left: 4px solid ${fb.color}; padding: 6px 12px; border-radius: 4px; margin-bottom: 10px;">
                        <span style="font-weight: 700; color: #1e293b; font-size: 13px;">${formNames[f]}</span>
                        <span style="background: ${fb.bg}; color: ${fb.color}; font-size: 11px; font-weight: 700; padding: 2px 7px; border-radius: 999px;">
                            ${fieldsForForm.length} รายการ
                        </span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 12px;">
            `;

            fieldsForForm.forEach(item => {
                const filled = isFieldFilled(data, item.key);
                let val = (data[item.key] !== undefined && data[item.key] !== null) ? data[item.key] : '';
                if (item.key === 'f1_gcs_total' && !val && data.f1_gcs_e && data.f1_gcs_v && data.f1_gcs_m) {
                    val = parseInt(data.f1_gcs_e, 10) + parseInt(data.f1_gcs_v, 10) + parseInt(data.f1_gcs_m, 10);
                }
                if (item.key === 'f4_gcs_total' && !val && data.f4_gcs_e && data.f4_gcs_v && data.f4_gcs_m) {
                    val = parseInt(data.f4_gcs_e, 10) + parseInt(data.f4_gcs_v, 10) + parseInt(data.f4_gcs_m, 10);
                }
                const isFocused = (focusKey === item.key);

                let statusBadge = filled ?
                    '<span style="background:#dcfce7; color:#15803d; font-size:10.5px; font-weight:700; padding:1px 6px; border-radius:4px;">✓ บันทึกแล้ว</span>' :
                    '<span style="background:#fee2e2; color:#b91c1c; font-size:10.5px; font-weight:700; padding:1px 6px; border-radius:4px;">⚠️ ช่องว่าง</span>';

                let inputHtml = '';
                if (item.type === 'select') {
                    inputHtml = `
                        <select class="blank-field-input" data-field-key="${item.key}" id="blank-input-${item.key}">
                            <option value="">-- กรุณาเลือก --</option>
                            ${item.options.map(opt => `<option value="${opt.value}" ${String(val) === String(opt.value) ? 'selected' : ''}>${opt.label}</option>`).join('')}
                        </select>
                    `;
                } else if (item.type === 'number') {
                    inputHtml = `
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <input type="number" class="blank-field-input" data-field-key="${item.key}" id="blank-input-${item.key}" value="${val}" ${item.min !== undefined ? `min="${item.min}"` : ''} ${item.max !== undefined ? `max="${item.max}"` : ''} ${item.step ? `step="${item.step}"` : 'step="any"'} placeholder="${item.placeholder || 'กรอกตัวเลข'}" style="flex: 1;">
                            ${item.unit ? `<span style="font-size: 11.5px; color: #64748b; font-weight: 600; white-space: nowrap;">${item.unit}</span>` : ''}
                        </div>
                    `;
                } else if (item.type === 'date') {
                    inputHtml = `
                        <input type="date" class="blank-field-input" data-field-key="${item.key}" id="blank-input-${item.key}" value="${val}">
                    `;
                } else if (item.type === 'time') {
                    inputHtml = `
                        <input type="time" class="blank-field-input" data-field-key="${item.key}" id="blank-input-${item.key}" value="${val}">
                    `;
                } else {
                    inputHtml = `
                        <input type="text" class="blank-field-input" data-field-key="${item.key}" id="blank-input-${item.key}" value="${val}" placeholder="${item.placeholder || 'กรอกข้อมูล...'}">
                    `;
                }

                formsHtml += `
                    <div class="blank-field-card ${isFocused ? 'pulse-focus' : ''}" style="border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px 12px; background: #ffffff;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px; gap: 6px;">
                            <div>
                                <div style="font-size: 10.5px; color: #64748b; font-weight: 600;">${item.category || item.formName}</div>
                                <div style="font-size: 12.5px; font-weight: 700; color: #1e293b; line-height: 1.3;">${item.label}</div>
                            </div>
                            <div>${statusBadge}</div>
                        </div>
                        <div style="margin-top: 4px;">
                            ${inputHtml}
                        </div>
                    </div>
                `;
            });

            formsHtml += `
                    </div>
                </div>
            `;
        }

        if (totalRenderedFields === 0) {
            formsHtml = `
                <div style="text-align: center; padding: 40px 20px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;">
                    <div style="font-size: 36px; margin-bottom: 8px;">🎉</div>
                    <div style="font-size: 16px; font-weight: 700; color: #15803d;">ข้อมูลเคสนี้ครบถ้วน 100% แล้ว!</div>
                    <div style="font-size: 13px; color: #166534; margin-top: 4px;">
                        ไม่มีตัวแปรที่ว่างอยู่ตามเกณฑ์วิจัย หากต้องการตรวจสอบหรือแก้ไขข้อมูลทั้งหมด ให้คลิกปุ่ม <b>"👁️ แสดงทุกช่อง"</b> ด้านบน
                    </div>
                </div>
            `;
        }

        bodyEl.innerHTML = formsHtml;

        if (focusKey) {
            setTimeout(() => {
                const targetInput = document.getElementById('blank-input-' + focusKey);
                if (targetInput) {
                    targetInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    targetInput.focus();
                }
            }, 200);
        }
    }

    function saveBlanksModalData() {
        if (!currentBlanksStudyId) return;
        const raw = localStorage.getItem('online_crf_case_' + currentBlanksStudyId);
        if (!raw) return;
        let data = JSON.parse(raw);

        const inputs = document.querySelectorAll('#fill-blanks-modal .blank-field-input');
        let savedCount = 0;

        inputs.forEach(inp => {
            const key = inp.getAttribute('data-field-key');
            if (!key) return;
            const val = inp.value.trim();
            if (data[key] !== val) {
                data[key] = val;
                savedCount++;
            }
            // Sync radio element IDs and remove stale sibling radio IDs
            const matchedRadio = document.querySelector(`input[type="radio"][name="${key}"][value="${val}"]`);
            if (matchedRadio && matchedRadio.id) {
                data[matchedRadio.id] = true;
            }
            document.querySelectorAll(`input[type="radio"][name="${key}"]`).forEach(r => {
                if (r.id && r.value !== val) {
                    delete data[r.id];
                }
            });
            // Auto calculate GCS components if GCS total entered
            if (key === 'f1_gcs_total' && val) {
                const tot = parseInt(val, 10);
                if (!isNaN(tot)) {
                    if (tot === 15 && (!data.f1_gcs_e || !data.f1_gcs_v || !data.f1_gcs_m)) {
                        data.f1_gcs_e = '4'; data.f1_gcs_v = '5'; data.f1_gcs_m = '6';
                    }
                }
            }
            if (key === 'f4_gcs_total' && val) {
                const tot = parseInt(val, 10);
                if (!isNaN(tot)) {
                    if (tot === 15 && (!data.f4_gcs_e || !data.f4_gcs_v || !data.f4_gcs_m)) {
                        data.f4_gcs_e = '4'; data.f4_gcs_v = '5'; data.f4_gcs_m = '6';
                    }
                }
            }
        });

        // Clean up conditional sub-fields if parent toggle is inactive
        if (data.f1_intubation !== '1') {
            delete data.f1_ett_no;
            delete data.f1_ett_time;
        }
        if (data.f1_inotropes !== '1') {
            delete data.f1_inotropes_name;
            delete data.f1_inotropes_dose;
        }

        localStorage.setItem('online_crf_case_' + currentBlanksStudyId, JSON.stringify(data));

        // If active case in background form is this same case, update via setFormData and calcAll
        const activeId = localStorage.getItem('online_crf_last_active_id');
        if (activeId === currentBlanksStudyId) {
            setFormData(data);
            if (typeof calcAll === 'function') {
                calcAll();
            }
        }

        // Show feedback message
        const feedbackEl = document.getElementById('blanks-save-feedback');
        if (feedbackEl) {
            feedbackEl.textContent = '✓ บันทึกข้อมูลสำเร็จเรียบร้อย (' + savedCount + ' ช่อง)';
            feedbackEl.style.display = 'block';
            setTimeout(() => { if (feedbackEl) feedbackEl.style.display = 'none'; }, 3000);
        }

        // Re-render admin dashboard live
        renderAdminDashboard();

        // Re-render blanks modal body to reflect new filled state
        renderBlanksModalBody(currentBlanksStudyId, currentBlanksShowAll);
    }
    """
