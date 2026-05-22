import React from "react";

if (typeof window !== "undefined" && process.env.NODE_ENV === "development") {
  const { default: wdyr } = require("@welldone-software/why-did-you-render");
  wdyr(React, {
    trackAllPureComponents: true,
    trackHooks: true,
  });
}