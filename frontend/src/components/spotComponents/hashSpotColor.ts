const colors = [
  "red",
  "orange",
  "yellow",
  "green",
  "teal",
  "blue",
  "cyan",
  "purple",
  "pink",
  "indigo",
  "lime",
];

export default function hashSpotColor(colorKey: number) {
  return colors[colorKey % colors.length];
}
