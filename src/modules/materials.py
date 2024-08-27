import glm
from modules.structures import Material

emerald = Material(
    "emerald",
    glm.vec3(0.0215, 0.1745, 0.0215),
    glm.vec3(0.07568, 0.61424, 0.07568),
    glm.vec3(0.633, 0.727811, 0.633),
    0.6, 
    0.7, 
    0.04,
    1.544
)

jade = Material(
    "jade",
    glm.vec3(0.135, 0.2225, 0.1575),
    glm.vec3(0.54, 0.89, 0.63),
    glm.vec3(0.316228),
    0.3, 
    0.7, 
    0.04,
    1.6
)

obsidian = Material(
    "obsidian",
    glm.vec3(0.05375, 0.05, 0.06625),
    glm.vec3(0.18275, 0.17, 0.22525),
    glm.vec3(0.332741, 0.328634, 0.346435),
    0.5, 
    0.8, 
    0.04,
    1.7
)

pearl = Material(
    "pearl",
    glm.vec3(0.25, 0.20725, 0.20725),
    glm.vec3(1, 0.829, 0.829),
    glm.vec3(0.296648),
    0.3, 
    0.8, 
    0.08,
    1.55
)

ruby = Material(
    "ruby",
    glm.vec3(0.1745, 0.01175, 0.01175),
    glm.vec3(0.61424, 0.04136, 0.04136),
    glm.vec3(0.727811, 0.626959, 0.626959),
    0.7, 
    0.8, 
    0.04,
    1.76
)

turquoise = Material(
    "turquoise",
    glm.vec3(0.1, 0.18725, 0.1745),
    glm.vec3(0.396, 0.74151, 0.69102),
    glm.vec3(0.297254, 0.30829, 0.306678),
    0.4, 
    0.7, 
    0.04,
    1.61
)

brass = Material(
    "brass",
    glm.vec3(0.329412, 0.223529, 0.027451),
    glm.vec3(0.780392, 0.568627, 0.113725),
    glm.vec3(0.992157, 0.941176, 0.807843),
    0.5, 
    0.0, 
    0.2, 
    1.5
)

bronze = Material(
    "bronze",
    glm.vec3(0.2125, 0.1275, 0.054),
    glm.vec3(0.714, 0.4284, 0.18144),
    glm.vec3(0.393548, 0.271906, 0.166721),
    0.4, 
    0.0, 
    0.2, 
    1.5
)

chrome = Material(
    "chrome",
    glm.vec3(0.25),
    glm.vec3(0.4),
    glm.vec3(0.774597),
    0.9, 
    0.0, 
    1.0,
    1.5
)

copper = Material(
    "copper",
    glm.vec3(0.19125, 0.0735, 0.0225),
    glm.vec3(0.7038, 0.27048, 0.0828),
    glm.vec3(0.256777, 0.137622, 0.086014),
    0.4, 
    0.0, 
    0.2, 
    1.3
)

gold = Material(
    "gold",
    glm.vec3(0.24725, 0.1995, 0.0745),
    glm.vec3(0.75164, 0.60648, 0.22648),
    glm.vec3(0.628281, 0.555802, 0.366065),
    0.8, 
    0.0, 
    0.4, 
    1.4
)

silver = Material(
    "silver",
    glm.vec3(0.19225),
    glm.vec3(0.50754),
    glm.vec3(0.508273),
    0.8, 
    0.0, 
    0.8, 
    1.5
)

black_plastic = Material(
    "black_plastic",
    glm.vec3(0.0),
    glm.vec3(0.01),
    glm.vec3(0.5),
    0.25,
    0.0, 
    0.04,
    1.5
)

cyan_plastic = Material(
    "cyan_plastic",
    glm.vec3(0.0, 0.1, 0.06),
    glm.vec3(0.0, 0.50980392, 0.50980392),
    glm.vec3(0.50196078),
    0.25,
    0.0, 
    0.04,
    1.5
)

green_plastic = Material(
    "green_plastic",
    glm.vec3(0.0),
    glm.vec3(0.1, 0.35, 0.1),
    glm.vec3(0.45, 0.55, 0.45),
    0.25,
    0.0, 
    0.04,
    1.5
)

red_plastic = Material(
    "red_plastic",
    glm.vec3(0.0),
    glm.vec3(0.5, 0.0, 0.0),
    glm.vec3(0.7, 0.6, 0.6),
    0.25,
    0.0, 
    0.04,
    1.5
)

white_plastic = Material(
    "white_plastic",
    glm.vec3(0.0),
    glm.vec3(0.55),
    glm.vec3(0.7),
    0.25,
    0.0, 
    0.04,
    1.5
)

yellow_plastic = Material(
    "yellow_plastic",
    glm.vec3(0.0),
    glm.vec3(0.5, 0.5, 0.0),
    glm.vec3(0.6, 0.6, 0.5),
    0.25,
    0.0, 
    0.04,
    1.5
)

black_rubber = Material(
    "black_rubber",
    glm.vec3(0.02),
    glm.vec3(0.01),
    glm.vec3(0.4),
    0.078125,
    0.0, 
    0.04,
     1.45
)

cyan_rubber = Material(
    "cyan_rubber",
    glm.vec3(0.0, 0.05, 0.05),
    glm.vec3(0.4, 0.5, 0.5),
    glm.vec3(0.04, 0.7, 0.7),
    0.078125,
    0.0, 
    0.04,
    1.5
)

green_rubber = Material(
    "green_rubber",
    glm.vec3(0.0, 0.05, 0.0),
    glm.vec3(0.4, 0.5, 0.4),
    glm.vec3(0.04, 0.7, 0.04),
    0.078125,
    0.0, 
    0.04,
    1.5
)

red_rubber = Material(
    "red_rubber",
    glm.vec3(0.05, 0.0, 0.0),
    glm.vec3(0.5, 0.4, 0.4),
    glm.vec3(0.7, 0.04, 0.04),
    0.078125,
    0.0, 
    0.04,
    1.5
)

white_rubber = Material(
    "white_rubber",
    glm.vec3(0.05),
    glm.vec3(0.5),
    glm.vec3(0.7),
    0.078125,
    0.0, 
    0.04,
    1.5
)

yellow_rubber = Material(
    "yellow_rubber",
    glm.vec3(0.05, 0.05, 0.0),
    glm.vec3(0.5, 0.5, 0.4),
    glm.vec3(0.7, 0.7, 0.04),
    0.078125,
    0.0, 
    0.04,
    1.5
)

glass = Material(
    "glass",
    glm.vec3(0.1),
    glm.vec3(0.5),
    glm.vec3(0.9),
    0.7,
    0.8, 
    0.5, 
    1.5
)


materials = {
    "emerald": emerald,
    "jade": jade,
    "obsidian": obsidian,
    "pearl": pearl,
    "ruby": ruby,
    "turquoise": turquoise,
    "brass": brass,
    "bronze": bronze,
    "chrome": chrome,
    "copper": copper,
    "gold": gold,
    "silver": silver,
    "black_plastic": black_plastic,
    "cyan_plastic": cyan_plastic,
    "green_plastic": green_plastic,
    "red_plastic": red_plastic,
    "white_plastic": white_plastic,
    "yellow_plastic": yellow_plastic,
    "black_rubber": black_rubber,
    "cyan_rubber": cyan_rubber,
    "green_rubber": green_rubber,
    "red_rubber": red_rubber,
    "white_rubber": white_rubber,
    "yellow_rubber": yellow_rubber,
    "glass": glass
}