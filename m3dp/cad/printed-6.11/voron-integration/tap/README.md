# TAP integration — verified CAD fit prototype

Read [TOP-TAP-PROTOTYPE.md](TOP-TAP-PROTOTYPE.md) for the 11 mm design, hardware and physical acceptance checks. The native model, two STEP files and four STL exports have passed the documented digital checks. The interface gauge is included separately. These parts have not been physically qualified.

For regeneration, run `BuildTopTapPrototype.FCMacro` in FreeCAD, run `ValidateTopTapAir.py` using PythonOCC, then run `VerifyTopTapPrototype.FCMacro` in FreeCAD. The independent airway receipt must match the exact rebuilt export hashes. The supplied model and exports have matching receipts. See `final11-source-freeze.json` and `top-native-validation.json`.

No third-party V2 reconstruction body is included. See [reference attribution](REFERENCE-ATTRIBUTION.md).
