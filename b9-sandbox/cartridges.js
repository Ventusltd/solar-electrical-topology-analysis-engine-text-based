export const CARTRIDGES = [
  {
    id: "fixed-1p",
    name: "Fixed tilt · 1 in portrait",
    version: "0.1.0",
    faces: 1,
    modulesHigh: 1,
    tracker: false,
    eastWest: false,
  },
  {
    id: "fixed-2p",
    name: "Fixed tilt · 2 in portrait",
    version: "0.1.0",
    faces: 1,
    modulesHigh: 2,
    tracker: false,
    eastWest: false,
  },
  {
    id: "east-west-1p",
    name: "East-west · 1 in portrait per face",
    version: "0.1.0",
    faces: 2,
    modulesHigh: 1,
    tracker: false,
    eastWest: true,
  },
  {
    id: "east-west-5p",
    name: "East-west · 5 in portrait per face",
    version: "0.1.0",
    faces: 2,
    modulesHigh: 5,
    tracker: false,
    eastWest: true,
  },
  {
    id: "legacy-6l",
    name: "Legacy fixed tilt · 6 in landscape",
    version: "0.1.0",
    faces: 1,
    modulesHigh: 6,
    tracker: false,
    eastWest: false,
    orientation: "landscape",
  },
  {
    id: "tracker-1p",
    name: "Tracker · 1 in portrait",
    version: "0.1.0",
    faces: 1,
    modulesHigh: 1,
    tracker: true,
    eastWest: false,
  },
  {
    id: "tracker-2p",
    name: "Tracker · 2 in portrait",
    version: "0.1.0",
    faces: 1,
    modulesHigh: 2,
    tracker: true,
    eastWest: false,
  },
];

export function getCartridge(id) {
  return CARTRIDGES.find((cartridge) => cartridge.id === id)
    ?? CARTRIDGES[0];
}
