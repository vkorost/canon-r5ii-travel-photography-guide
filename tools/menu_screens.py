# -*- coding: utf-8 -*-
"""Content for the drawn menu screens.

Item names, page numbers and tab names come from the Mark II's own menu
structure (``working/menu-paths.json``, built from the manual's index links);
option lists come from the item entries in Appendix B. Values shown are the
camera's defaults unless the figure's caption is about a changed one.

``kind="options"`` draws a setting's option list; the default is a secondary
tab page. Row states: ``sel`` the highlighted row, ``dim`` grayed out,
``cur`` the option currently in force, ``on``/``off`` a tick box.
"""

SCREENS = [
    # ---------------------------------------------------------- Shooting
    dict(id="m_shutter_control", tab="shooting", page=6, of=9,
         name="Shutter control",
         items=[("Drive mode", "", ""),
                ("Pre-cont. shooting", "Disable", ""),
                ("Interval timer", "Disable", ""),
                ("Bulb timer", "Disable", "dim"),
                ("Silent shutter function", "OFF", ""),
                ("Shutter mode", "Elec. 1st-curtain", "sel"),
                ("Release shutter without card", "OFF", "")]),

    dict(id="m_exposure_page", tab="shooting", page=2, of=9, name="Exposure",
         items=[("Expo.comp./AEB", "-3..0..+3", ""),
                ("ISO speed settings", "", ""),
                ("Anti-flicker shoot.", "Disable", "sel"),
                ("HF anti-flicker shooting", "Disable", ""),
                ("External Speedlite control", "", ""),
                ("Metering mode", "", ""),
                ("Detect priority AE while AF", "Disable", "")]),

    dict(id="m_metering", kind="options", name="Metering mode",
         where="Shooting 2/9",
         items=[("Evaluative metering", "", "cur"),
                ("Partial metering", "", ""),
                ("Spot metering", "", "sel"),
                ("Center-weighted average", "", "")]),

    dict(id="m_iso_settings", kind="options", name="ISO speed settings",
         where="Shooting 2/9",
         items=[("ISO speed", "AUTO", ""),
                ("ISO speed range", "100-102400", ""),
                ("Auto range", "100-12800", "sel"),
                ("Min. shutter spd.", "Auto", "")]),

    dict(id="m_cropping", kind="options", name="Cropping/aspect ratio",
         where="Shooting 1/9",
         items=[("Full-frame", "", "cur"),
                ("1.6x (crop)", "", "sel"),
                ("1:1 (aspect ratio)", "", ""),
                ("4:3 (aspect ratio)", "", ""),
                ("16:9 (aspect ratio)", "", "")]),

    dict(id="m_lens_aberration", kind="options",
         name="Lens aberration correction", where="Shooting 4/9",
         items=[("Peripheral illum corr", "Enable", ""),
                ("Distortion correction", "Disable", ""),
                ("Digital Lens Optimizer", "Standard", "sel"),
                ("Chromatic aberr corr", "Enable", ""),
                ("Diffraction correction", "Enable", "")]),

    dict(id="m_high_iso_nr", kind="options", name="High ISO speed NR",
         where="Shooting 4/9",
         items=[("Disable", "", ""), ("Low", "", ""),
                ("Standard", "", "cur"), ("High", "", "sel")]),

    dict(id="m_focus_bracketing", kind="options", name="Focus bracketing",
         where="Shooting 5/9",
         items=[("Focus bracketing", "Enable", "sel"),
                ("Number of shots", "100", ""),
                ("Focus increment", "4", ""),
                ("Exposure smoothing", "Enable", ""),
                ("Depth composite", "Disable", "")]),

    dict(id="m_is_mode", tab="shooting", page=7, of=9,
         name="Assist shooting",
         items=[("IS (Image Stabilizer) mode", "", "dim"),
                ("Customize Quick Controls", "", ""),
                ("Metering timer", "8 sec.", "")]),

    dict(id="m_metering_timer", kind="options", name="Metering timer",
         where="Shooting 7/9",
         items=[("4 sec.", "", ""), ("8 sec.", "", "cur"),
                ("16 sec.", "", "sel"), ("30 sec.", "", ""),
                ("1 min.", "", ""), ("10 min.", "", ""),
                ("30 min.", "", "")]),

    dict(id="m_display_sim", kind="options", name="Display simulation",
         where="Shooting 8/9",
         items=[("Disable", "", ""),
                ("Exposure", "", "cur"),
                ("Expo.+DoF", "", "sel"),
                ("Depth of field", "", "")]),

    dict(id="m_shooting_info", kind="options", name="Shooting info. disp.",
         where="Shooting 9/9",
         items=[("Screen info. settings", "", "sel"),
                ("VF info/toggle settings", "", ""),
                ("VF vertical display", "Enable", ""),
                ("Grid display", "Off", ""),
                ("Histogram disp", "Brightness", ""),
                ("Lens info display", "", ""),
                ("Clear settings", "", "")]),

    dict(id="m_vf_info", kind="options", name="VF info/toggle settings",
         where="Shooting info. disp.",
         items=[("Screen 1", "", "on"), ("Screen 2", "", "on"),
                ("Screen 3", "", "off"), ("Screen 4", "", "off"),
                ("Screen 5", "", "off")]),

    dict(id="m_grid", kind="options", name="Grid display",
         where="Shooting info. disp.",
         items=[("Off", "", "cur"), ("3x3", "", ""),
                ("6x4", "", "sel"), ("3x3+diag", "", "")]),

    # ---------------------------------------------------------- Autofocus
    dict(id="m_af_operation_page", tab="af", page=1, of=7,
         name="AF operation/area",
         items=[("AF operation", "ONE SHOT", ""),
                ("AF area", "", ""),
                ("Whole area tracking Servo AF", "On", "sel"),
                ("Focus mode", "AF", "")]),

    dict(id="m_af_area", kind="options", name="AF area",
         where="Autofocus 1/7",
         items=[("Spot AF", "", ""),
                ("1-point AF", "", "cur"),
                ("Expand AF area", "", ""),
                ("Flexible Zone AF 1", "", "sel"),
                ("Flexible Zone AF 2", "", ""),
                ("Flexible Zone AF 3", "", ""),
                ("Whole area AF", "", "")]),

    dict(id="m_subject_detect", kind="options", name="Subject to detect",
         where="Autofocus 2/7",
         items=[("People", "", "cur"), ("Animals", "", ""),
                ("Vehicles", "", "sel"), ("None", "", "")]),

    dict(id="m_eye_detection", kind="options", name="Eye detection",
         where="Autofocus 2/7",
         items=[("Auto", "", "cur"), ("Right eye", "", ""),
                ("Left eye", "", "sel"), ("Disable", "", "")]),

    dict(id="m_servo_cases", tab="af", page=3, of=7,
         name="Servo AF character.",
         items=[("Case Auto", "", "sel"),
                ("Case Auto character.", "Standard", ""),
                ("Case Manual", "", ""),
                ("Tracking sensitivity", "0", "dim"),
                ("Accel./decel. tracking", "0", "dim"),
                ("Case Special", "", "")]),

    dict(id="m_lens_emf", kind="options", name="Lens electronic MF",
         where="Autofocus 6/7",
         items=[("Disable after One-Shot AF", "", ""),
                ("Enable after One-Shot AF", "", "cur"),
                ("Disable in AF mode", "", "sel"),
                ("Enable in AF mode", "", "")]),

    dict(id="m_custom_mode", kind="options",
         name="Custom shooting mode (C1-C3)", where="Set-up 5/6",
         items=[("Register settings", "", "sel"),
                ("Clear settings", "", ""),
                ("Auto update set.", "Disable", "")]),

    # ------------------------------------------ Control customization
    dict(id="m_control_custom_page", tab="control", page=1, of=4,
         name="Customized controls when shooting",
         items=[("Customize buttons for shooting", "", "sel"),
                ("Customize dials/control ring", "-", ""),
                ("direction to set Tv/Av", "", ""),
                ("Switch dials when shooting", "OFF", ""),
                ("Touch Shutter", "Disable", ""),
                ("Multi function lock", "-", "")]),

    dict(id="m_mf_lock", kind="options", name="Multi function lock",
         where="Control cust. 1/4",
         items=[("Main dial", "", "on"),
                ("Quick control dial 1", "", "on"),
                ("Quick control dial 2", "", "on"),
                ("Multi-controller", "", "on"),
                ("Control ring", "", "off"),
                ("Touch control", "", "on")]),

    dict(id="m_touch_drag", kind="options", name="Touch & drag AF settings",
         where="Control cust. 2/4",
         items=[("Touch & drag AF", "Enable", "sel"),
                ("Positioning method", "Relative", ""),
                ("Active touch area", "Right", "")]),

    dict(id="m_eye_control", kind="options", name="Eye control",
         where="Control cust. 4/4",
         items=[("Eye control", "Enable", "sel"),
                ("Calibration", "", ""),
                ("Pointer display", "On", ""),
                ("Pointer disp. during Servo", "Off", "")]),

    # ---------------------------------------------------------- My Menu
    dict(id="m_mymenu_page", tab="mymenu", page=1, of=1,
         name="My Menu management",
         items=[("Add My Menu tab", "", "sel"),
                ("Delete all My Menu tabs", "", ""),
                ("Delete all items", "", ""),
                ("Menu display", "Normal display", "")]),

    dict(id="m_mymenu_config", kind="options", name="Configure MY MENU1",
         where="My Menu 1/1",
         items=[("Select items to register", "", "sel"),
                ("Sort registered items", "", ""),
                ("Delete selected items", "", ""),
                ("Delete all items on tab", "", ""),
                ("Delete tab", "", ""),
                ("Rename tab", "", "")]),
]
