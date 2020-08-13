import process from "process";

import Port from "./library/port";
import BetterMixer from "./library/betterMixer";
import CellTrapL from "./library/celltrapL";
import Chamber from "./library/chamber";
import Channel from "./library/channel";
import Connection from "./library/connection";
import CurvedMixer from "./library/curvedMixer";
import DiamondReactionChamber from "./library/diamondReactionChamber";
import DropletGenerator from "./library/dropletGenerator";
import GradientGenerator from "./library/gradientGenerator";
import Mux from "./library/mux";
import Pump from "./library/pump";
import Pump3D from "./library/pump3D";
import RectValve from "./library/rectValve";
import RotaryMixer from "./library/rotaryMixer";
import Transposer from "./library/transposer";
import Valve from "./library/valve";
import Valve3D from "./library/valve3D";
import Via from "./library/via";
import Tree from "./library/tree";
import YTree from "./library/ytree";
import Node from "./library/node";

import paper from "paper";

paper.setup([640, 480]);

let primitive_map = new Map();

let port = new Port();
let better_mixer = new BetterMixer();
let cell_trap_l = new CellTrapL();
let chamber = new Chamber();
let channel = new Channel();
let connection = new Connection();
let curved_mixer = new CurvedMixer();
let diamond_reaction_chamber = new DiamondReactionChamber();
let droplet_generator = new DropletGenerator();
let gradient_generator = new GradientGenerator();
let mux = new Mux();
let pump = new Pump();
let pump3D = new Pump3D();
let rect_valve = new RectValve();
let rotary_mixer = new RotaryMixer();
let transposer = new Transposer();
let valve = new Valve();
let valve3D = new Valve3D();
let via = new Via();
let tree = new Tree();
let ytree = new YTree();
let node = new Node();

primitive_map.set(port.mint.replace(/\s/g, ''), port);
primitive_map.set(better_mixer.mint.replace(/\s/g, ''), better_mixer);
primitive_map.set(cell_trap_l.mint.replace(/\s/g, ''), cell_trap_l);
primitive_map.set(chamber.mint.replace(/\s/g, ''), chamber);
primitive_map.set(channel.mint.replace(/\s/g, ''), channel);
primitive_map.set(connection.mint.replace(/\s/g, ''), connection);
primitive_map.set(curved_mixer.mint.replace(/\s/g, ''), curved_mixer);
primitive_map.set(diamond_reaction_chamber.mint.replace(/\s/g, ''), diamond_reaction_chamber);
primitive_map.set(droplet_generator.mint.replace(/\s/g, ''), droplet_generator);
primitive_map.set(gradient_generator.mint.replace(/\s/g, ''), gradient_generator);
primitive_map.set(mux.mint.replace(/\s/g, ''), mux);
primitive_map.set(pump.mint.replace(/\s/g, ''), pump);
primitive_map.set(pump3D.mint.replace(/\s/g, ''), pump3D);
primitive_map.set(rect_valve.mint.replace(/\s/g, ''), rect_valve);
primitive_map.set(rotary_mixer.mint.replace(/\s/g, ''), rotary_mixer);
primitive_map.set(transposer.mint.replace(/\s/g, ''), transposer);
primitive_map.set(valve.mint.replace(/\s/g, ''), valve);
primitive_map.set(valve3D.mint.replace(/\s/g, ''), valve3D);
primitive_map.set(via.mint.replace(/\s/g, ''), via);
primitive_map.set(tree.mint.replace(/\s/g, ''), tree);
primitive_map.set(ytree.mint.replace(/\s/g, ''), ytree);
primitive_map.set(node.mint.replace(/\s/g, ''), node);

// console.log(primitive_map.keys());

let primitive = process.argv[2];
let command = process.argv[3];

let technology = primitive_map.get(primitive.replace(/\s/g, ''));

if (command === "dimension"){
    let params_text = process.argv[4];

    let params = JSON.parse(params_text);
    params["position"] = [0,0];
    params["color"] = "#FFF";

    let feature = technology.render2D(params);
    let xspan = feature.bounds.width;
    let yspan = feature.bounds.height;
    // console.log("Dimensions:",xspan, yspan);
    console.log(JSON.stringify({"x-span":xspan, "y-span":yspan}));

}else if(command === "defaults"){
    let defaults = technology.defaults;

    console.log(JSON.stringify(defaults));
}



// console.log("Map; ", primitive_map);