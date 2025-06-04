const { Router } = require("express");
const router = Router();

router.get("/", async (req, res) => {
  res.render("ota", {
    requerimientos: [
      { id: "VDD", nombre: "VDD (V)" },
      { id: "VSS", nombre: "VSS (V)" },
      { id: "VIC_MAX", nombre: "VIC Máx (V)" },
      { id: "VIC_MIN", nombre: "VIC Mín (V)" },
      { id: "AVD", nombre: "AVD (ganancia)" },
      { id: "SR", nombre: "SR (V/µs)" },
      { id: "CL", nombre: "CL (pF)" },
      { id: "frec_c", nombre: "frec_c (Hz)" },
      { id: "Pmax", nombre: "Pmax (µW)" },
    ],
    parametros: [
      { id: "VTN", nombre: "VTN (V)" },
      { id: "VTP", nombre: "VTP (V)" },
      { id: "TOXN", nombre: "TOXN (nm)" },
      { id: "TOXP", nombre: "TOXP (nm)" },
      { id: "Uo_N", nombre: "Uo_N (CM^2 /VS)"},
      { id: "Uo_P", nombre: "Uo_P (CM^2 /VS)"},
      { id: "EPSO", nombre: "EPSO (F /M)"},
      { id: "ER_SIO2", nombre: "ER_SIO2"}
    ]
  });
});

module.exports = router;