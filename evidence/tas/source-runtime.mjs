import {createRequire} from 'node:module'; const require=createRequire(import.meta.url);
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __require = /* @__PURE__ */ ((x) => typeof require !== "undefined" ? require : typeof Proxy !== "undefined" ? new Proxy(x, {
  get: (a, b) => (typeof require !== "undefined" ? require : a)[b]
}) : x)(function(x) {
  if (typeof require !== "undefined") return require.apply(this, arguments);
  throw Error('Dynamic require of "' + x + '" is not supported');
});
var __commonJS = (cb, mod) => function __require2() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// pinned:artifacts/tas-phase3a/runtime/node_modules/@noble/hashes/_u64.js
var require_u64 = __commonJS({
  "pinned:artifacts/tas-phase3a/runtime/node_modules/@noble/hashes/_u64.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.toBig = exports.shrSL = exports.shrSH = exports.rotrSL = exports.rotrSH = exports.rotrBL = exports.rotrBH = exports.rotr32L = exports.rotr32H = exports.rotlSL = exports.rotlSH = exports.rotlBL = exports.rotlBH = exports.add5L = exports.add5H = exports.add4L = exports.add4H = exports.add3L = exports.add3H = void 0;
    exports.add = add;
    exports.fromBig = fromBig;
    exports.split = split;
    var U32_MASK64 = /* @__PURE__ */ BigInt(2 ** 32 - 1);
    var _32n = /* @__PURE__ */ BigInt(32);
    function fromBig(n, le = false) {
      if (le)
        return { h: Number(n & U32_MASK64), l: Number(n >> _32n & U32_MASK64) };
      return { h: Number(n >> _32n & U32_MASK64) | 0, l: Number(n & U32_MASK64) | 0 };
    }
    function split(lst, le = false) {
      const len = lst.length;
      let Ah = new Uint32Array(len);
      let Al = new Uint32Array(len);
      for (let i = 0; i < len; i++) {
        const { h, l } = fromBig(lst[i], le);
        [Ah[i], Al[i]] = [h, l];
      }
      return [Ah, Al];
    }
    var toBig = (h, l) => BigInt(h >>> 0) << _32n | BigInt(l >>> 0);
    exports.toBig = toBig;
    var shrSH = (h, _l, s) => h >>> s;
    exports.shrSH = shrSH;
    var shrSL = (h, l, s) => h << 32 - s | l >>> s;
    exports.shrSL = shrSL;
    var rotrSH = (h, l, s) => h >>> s | l << 32 - s;
    exports.rotrSH = rotrSH;
    var rotrSL = (h, l, s) => h << 32 - s | l >>> s;
    exports.rotrSL = rotrSL;
    var rotrBH = (h, l, s) => h << 64 - s | l >>> s - 32;
    exports.rotrBH = rotrBH;
    var rotrBL = (h, l, s) => h >>> s - 32 | l << 64 - s;
    exports.rotrBL = rotrBL;
    var rotr32H = (_h, l) => l;
    exports.rotr32H = rotr32H;
    var rotr32L = (h, _l) => h;
    exports.rotr32L = rotr32L;
    var rotlSH = (h, l, s) => h << s | l >>> 32 - s;
    exports.rotlSH = rotlSH;
    var rotlSL = (h, l, s) => l << s | h >>> 32 - s;
    exports.rotlSL = rotlSL;
    var rotlBH = (h, l, s) => l << s - 32 | h >>> 64 - s;
    exports.rotlBH = rotlBH;
    var rotlBL = (h, l, s) => h << s - 32 | l >>> 64 - s;
    exports.rotlBL = rotlBL;
    function add(Ah, Al, Bh, Bl) {
      const l = (Al >>> 0) + (Bl >>> 0);
      return { h: Ah + Bh + (l / 2 ** 32 | 0) | 0, l: l | 0 };
    }
    var add3L = (Al, Bl, Cl) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0);
    exports.add3L = add3L;
    var add3H = (low, Ah, Bh, Ch) => Ah + Bh + Ch + (low / 2 ** 32 | 0) | 0;
    exports.add3H = add3H;
    var add4L = (Al, Bl, Cl, Dl) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0) + (Dl >>> 0);
    exports.add4L = add4L;
    var add4H = (low, Ah, Bh, Ch, Dh) => Ah + Bh + Ch + Dh + (low / 2 ** 32 | 0) | 0;
    exports.add4H = add4H;
    var add5L = (Al, Bl, Cl, Dl, El) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0) + (Dl >>> 0) + (El >>> 0);
    exports.add5L = add5L;
    var add5H = (low, Ah, Bh, Ch, Dh, Eh) => Ah + Bh + Ch + Dh + Eh + (low / 2 ** 32 | 0) | 0;
    exports.add5H = add5H;
    var u64 = {
      fromBig,
      split,
      toBig,
      shrSH,
      shrSL,
      rotrSH,
      rotrSL,
      rotrBH,
      rotrBL,
      rotr32H,
      rotr32L,
      rotlSH,
      rotlSL,
      rotlBH,
      rotlBL,
      add,
      add3L,
      add3H,
      add4L,
      add4H,
      add5H,
      add5L
    };
    exports.default = u64;
  }
});

// pinned:artifacts/tas-phase3a/runtime/node_modules/@noble/hashes/cryptoNode.js
var require_cryptoNode = __commonJS({
  "pinned:artifacts/tas-phase3a/runtime/node_modules/@noble/hashes/cryptoNode.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.crypto = void 0;
    var nc = __require("node:crypto");
    exports.crypto = nc && typeof nc === "object" && "webcrypto" in nc ? nc.webcrypto : nc && typeof nc === "object" && "randomBytes" in nc ? nc : void 0;
  }
});

// pinned:artifacts/tas-phase3a/runtime/node_modules/@noble/hashes/utils.js
var require_utils = __commonJS({
  "pinned:artifacts/tas-phase3a/runtime/node_modules/@noble/hashes/utils.js"(exports) {
    "use strict";
    /*! noble-hashes - MIT License (c) 2022 Paul Miller (paulmillr.com) */
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.wrapXOFConstructorWithOpts = exports.wrapConstructorWithOpts = exports.wrapConstructor = exports.Hash = exports.nextTick = exports.swap32IfBE = exports.byteSwapIfBE = exports.swap8IfBE = exports.isLE = void 0;
    exports.isBytes = isBytes;
    exports.anumber = anumber;
    exports.abytes = abytes;
    exports.ahash = ahash;
    exports.aexists = aexists;
    exports.aoutput = aoutput;
    exports.u8 = u8;
    exports.u32 = u32;
    exports.clean = clean;
    exports.createView = createView;
    exports.rotr = rotr;
    exports.rotl = rotl;
    exports.byteSwap = byteSwap;
    exports.byteSwap32 = byteSwap32;
    exports.bytesToHex = bytesToHex2;
    exports.hexToBytes = hexToBytes2;
    exports.asyncLoop = asyncLoop;
    exports.utf8ToBytes = utf8ToBytes;
    exports.bytesToUtf8 = bytesToUtf8;
    exports.toBytes = toBytes2;
    exports.kdfInputToBytes = kdfInputToBytes;
    exports.concatBytes = concatBytes;
    exports.checkOpts = checkOpts;
    exports.createHasher = createHasher;
    exports.createOptHasher = createOptHasher;
    exports.createXOFer = createXOFer;
    exports.randomBytes = randomBytes;
    var crypto_1 = require_cryptoNode();
    function isBytes(a) {
      return a instanceof Uint8Array || ArrayBuffer.isView(a) && a.constructor.name === "Uint8Array";
    }
    function anumber(n) {
      if (!Number.isSafeInteger(n) || n < 0)
        throw new Error("positive integer expected, got " + n);
    }
    function abytes(b, ...lengths) {
      if (!isBytes(b))
        throw new Error("Uint8Array expected");
      if (lengths.length > 0 && !lengths.includes(b.length))
        throw new Error("Uint8Array expected of length " + lengths + ", got length=" + b.length);
    }
    function ahash(h) {
      if (typeof h !== "function" || typeof h.create !== "function")
        throw new Error("Hash should be wrapped by utils.createHasher");
      anumber(h.outputLen);
      anumber(h.blockLen);
    }
    function aexists(instance, checkFinished = true) {
      if (instance.destroyed)
        throw new Error("Hash instance has been destroyed");
      if (checkFinished && instance.finished)
        throw new Error("Hash#digest() has already been called");
    }
    function aoutput(out, instance) {
      abytes(out);
      const min = instance.outputLen;
      if (out.length < min) {
        throw new Error("digestInto() expects output buffer of length at least " + min);
      }
    }
    function u8(arr) {
      return new Uint8Array(arr.buffer, arr.byteOffset, arr.byteLength);
    }
    function u32(arr) {
      return new Uint32Array(arr.buffer, arr.byteOffset, Math.floor(arr.byteLength / 4));
    }
    function clean(...arrays) {
      for (let i = 0; i < arrays.length; i++) {
        arrays[i].fill(0);
      }
    }
    function createView(arr) {
      return new DataView(arr.buffer, arr.byteOffset, arr.byteLength);
    }
    function rotr(word, shift) {
      return word << 32 - shift | word >>> shift;
    }
    function rotl(word, shift) {
      return word << shift | word >>> 32 - shift >>> 0;
    }
    exports.isLE = (() => new Uint8Array(new Uint32Array([287454020]).buffer)[0] === 68)();
    function byteSwap(word) {
      return word << 24 & 4278190080 | word << 8 & 16711680 | word >>> 8 & 65280 | word >>> 24 & 255;
    }
    exports.swap8IfBE = exports.isLE ? (n) => n : (n) => byteSwap(n);
    exports.byteSwapIfBE = exports.swap8IfBE;
    function byteSwap32(arr) {
      for (let i = 0; i < arr.length; i++) {
        arr[i] = byteSwap(arr[i]);
      }
      return arr;
    }
    exports.swap32IfBE = exports.isLE ? (u) => u : byteSwap32;
    var hasHexBuiltin = /* @__PURE__ */ (() => (
      // @ts-ignore
      typeof Uint8Array.from([]).toHex === "function" && typeof Uint8Array.fromHex === "function"
    ))();
    var hexes2 = /* @__PURE__ */ Array.from({ length: 256 }, (_, i) => i.toString(16).padStart(2, "0"));
    function bytesToHex2(bytes) {
      abytes(bytes);
      if (hasHexBuiltin)
        return bytes.toHex();
      let hex = "";
      for (let i = 0; i < bytes.length; i++) {
        hex += hexes2[bytes[i]];
      }
      return hex;
    }
    var asciis = { _0: 48, _9: 57, A: 65, F: 70, a: 97, f: 102 };
    function asciiToBase16(ch) {
      if (ch >= asciis._0 && ch <= asciis._9)
        return ch - asciis._0;
      if (ch >= asciis.A && ch <= asciis.F)
        return ch - (asciis.A - 10);
      if (ch >= asciis.a && ch <= asciis.f)
        return ch - (asciis.a - 10);
      return;
    }
    function hexToBytes2(hex) {
      if (typeof hex !== "string")
        throw new Error("hex string expected, got " + typeof hex);
      if (hasHexBuiltin)
        return Uint8Array.fromHex(hex);
      const hl = hex.length;
      const al = hl / 2;
      if (hl % 2)
        throw new Error("hex string expected, got unpadded hex of length " + hl);
      const array = new Uint8Array(al);
      for (let ai = 0, hi = 0; ai < al; ai++, hi += 2) {
        const n1 = asciiToBase16(hex.charCodeAt(hi));
        const n2 = asciiToBase16(hex.charCodeAt(hi + 1));
        if (n1 === void 0 || n2 === void 0) {
          const char = hex[hi] + hex[hi + 1];
          throw new Error('hex string expected, got non-hex character "' + char + '" at index ' + hi);
        }
        array[ai] = n1 * 16 + n2;
      }
      return array;
    }
    var nextTick = async () => {
    };
    exports.nextTick = nextTick;
    async function asyncLoop(iters, tick, cb) {
      let ts = Date.now();
      for (let i = 0; i < iters; i++) {
        cb(i);
        const diff = Date.now() - ts;
        if (diff >= 0 && diff < tick)
          continue;
        await (0, exports.nextTick)();
        ts += diff;
      }
    }
    function utf8ToBytes(str) {
      if (typeof str !== "string")
        throw new Error("string expected");
      return new Uint8Array(new TextEncoder().encode(str));
    }
    function bytesToUtf8(bytes) {
      return new TextDecoder().decode(bytes);
    }
    function toBytes2(data) {
      if (typeof data === "string")
        data = utf8ToBytes(data);
      abytes(data);
      return data;
    }
    function kdfInputToBytes(data) {
      if (typeof data === "string")
        data = utf8ToBytes(data);
      abytes(data);
      return data;
    }
    function concatBytes(...arrays) {
      let sum = 0;
      for (let i = 0; i < arrays.length; i++) {
        const a = arrays[i];
        abytes(a);
        sum += a.length;
      }
      const res = new Uint8Array(sum);
      for (let i = 0, pad2 = 0; i < arrays.length; i++) {
        const a = arrays[i];
        res.set(a, pad2);
        pad2 += a.length;
      }
      return res;
    }
    function checkOpts(defaults, opts) {
      if (opts !== void 0 && {}.toString.call(opts) !== "[object Object]")
        throw new Error("options should be object or undefined");
      const merged = Object.assign(defaults, opts);
      return merged;
    }
    var Hash = class {
    };
    exports.Hash = Hash;
    function createHasher(hashCons) {
      const hashC = (msg) => hashCons().update(toBytes2(msg)).digest();
      const tmp = hashCons();
      hashC.outputLen = tmp.outputLen;
      hashC.blockLen = tmp.blockLen;
      hashC.create = () => hashCons();
      return hashC;
    }
    function createOptHasher(hashCons) {
      const hashC = (msg, opts) => hashCons(opts).update(toBytes2(msg)).digest();
      const tmp = hashCons({});
      hashC.outputLen = tmp.outputLen;
      hashC.blockLen = tmp.blockLen;
      hashC.create = (opts) => hashCons(opts);
      return hashC;
    }
    function createXOFer(hashCons) {
      const hashC = (msg, opts) => hashCons(opts).update(toBytes2(msg)).digest();
      const tmp = hashCons({});
      hashC.outputLen = tmp.outputLen;
      hashC.blockLen = tmp.blockLen;
      hashC.create = (opts) => hashCons(opts);
      return hashC;
    }
    exports.wrapConstructor = createHasher;
    exports.wrapConstructorWithOpts = createOptHasher;
    exports.wrapXOFConstructorWithOpts = createXOFer;
    function randomBytes(bytesLength = 32) {
      if (crypto_1.crypto && typeof crypto_1.crypto.getRandomValues === "function") {
        return crypto_1.crypto.getRandomValues(new Uint8Array(bytesLength));
      }
      if (crypto_1.crypto && typeof crypto_1.crypto.randomBytes === "function") {
        return Uint8Array.from(crypto_1.crypto.randomBytes(bytesLength));
      }
      throw new Error("crypto.getRandomValues must be defined");
    }
  }
});

// pinned:artifacts/tas-phase3a/runtime/node_modules/@noble/hashes/sha3.js
var require_sha3 = __commonJS({
  "pinned:artifacts/tas-phase3a/runtime/node_modules/@noble/hashes/sha3.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.shake256 = exports.shake128 = exports.keccak_512 = exports.keccak_384 = exports.keccak_256 = exports.keccak_224 = exports.sha3_512 = exports.sha3_384 = exports.sha3_256 = exports.sha3_224 = exports.Keccak = void 0;
    exports.keccakP = keccakP;
    var _u64_ts_1 = require_u64();
    var utils_ts_1 = require_utils();
    var _0n = BigInt(0);
    var _1n = BigInt(1);
    var _2n = BigInt(2);
    var _7n = BigInt(7);
    var _256n = BigInt(256);
    var _0x71n = BigInt(113);
    var SHA3_PI = [];
    var SHA3_ROTL = [];
    var _SHA3_IOTA = [];
    for (let round = 0, R = _1n, x = 1, y = 0; round < 24; round++) {
      [x, y] = [y, (2 * x + 3 * y) % 5];
      SHA3_PI.push(2 * (5 * y + x));
      SHA3_ROTL.push((round + 1) * (round + 2) / 2 % 64);
      let t = _0n;
      for (let j = 0; j < 7; j++) {
        R = (R << _1n ^ (R >> _7n) * _0x71n) % _256n;
        if (R & _2n)
          t ^= _1n << (_1n << /* @__PURE__ */ BigInt(j)) - _1n;
      }
      _SHA3_IOTA.push(t);
    }
    var IOTAS = (0, _u64_ts_1.split)(_SHA3_IOTA, true);
    var SHA3_IOTA_H = IOTAS[0];
    var SHA3_IOTA_L = IOTAS[1];
    var rotlH = (h, l, s) => s > 32 ? (0, _u64_ts_1.rotlBH)(h, l, s) : (0, _u64_ts_1.rotlSH)(h, l, s);
    var rotlL = (h, l, s) => s > 32 ? (0, _u64_ts_1.rotlBL)(h, l, s) : (0, _u64_ts_1.rotlSL)(h, l, s);
    function keccakP(s, rounds = 24) {
      const B = new Uint32Array(5 * 2);
      for (let round = 24 - rounds; round < 24; round++) {
        for (let x = 0; x < 10; x++)
          B[x] = s[x] ^ s[x + 10] ^ s[x + 20] ^ s[x + 30] ^ s[x + 40];
        for (let x = 0; x < 10; x += 2) {
          const idx1 = (x + 8) % 10;
          const idx0 = (x + 2) % 10;
          const B0 = B[idx0];
          const B1 = B[idx0 + 1];
          const Th = rotlH(B0, B1, 1) ^ B[idx1];
          const Tl = rotlL(B0, B1, 1) ^ B[idx1 + 1];
          for (let y = 0; y < 50; y += 10) {
            s[x + y] ^= Th;
            s[x + y + 1] ^= Tl;
          }
        }
        let curH = s[2];
        let curL = s[3];
        for (let t = 0; t < 24; t++) {
          const shift = SHA3_ROTL[t];
          const Th = rotlH(curH, curL, shift);
          const Tl = rotlL(curH, curL, shift);
          const PI = SHA3_PI[t];
          curH = s[PI];
          curL = s[PI + 1];
          s[PI] = Th;
          s[PI + 1] = Tl;
        }
        for (let y = 0; y < 50; y += 10) {
          for (let x = 0; x < 10; x++)
            B[x] = s[y + x];
          for (let x = 0; x < 10; x++)
            s[y + x] ^= ~B[(x + 2) % 10] & B[(x + 4) % 10];
        }
        s[0] ^= SHA3_IOTA_H[round];
        s[1] ^= SHA3_IOTA_L[round];
      }
      (0, utils_ts_1.clean)(B);
    }
    var Keccak = class _Keccak extends utils_ts_1.Hash {
      // NOTE: we accept arguments in bytes instead of bits here.
      constructor(blockLen, suffix, outputLen, enableXOF = false, rounds = 24) {
        super();
        this.pos = 0;
        this.posOut = 0;
        this.finished = false;
        this.destroyed = false;
        this.enableXOF = false;
        this.blockLen = blockLen;
        this.suffix = suffix;
        this.outputLen = outputLen;
        this.enableXOF = enableXOF;
        this.rounds = rounds;
        (0, utils_ts_1.anumber)(outputLen);
        if (!(0 < blockLen && blockLen < 200))
          throw new Error("only keccak-f1600 function is supported");
        this.state = new Uint8Array(200);
        this.state32 = (0, utils_ts_1.u32)(this.state);
      }
      clone() {
        return this._cloneInto();
      }
      keccak() {
        (0, utils_ts_1.swap32IfBE)(this.state32);
        keccakP(this.state32, this.rounds);
        (0, utils_ts_1.swap32IfBE)(this.state32);
        this.posOut = 0;
        this.pos = 0;
      }
      update(data) {
        (0, utils_ts_1.aexists)(this);
        data = (0, utils_ts_1.toBytes)(data);
        (0, utils_ts_1.abytes)(data);
        const { blockLen, state } = this;
        const len = data.length;
        for (let pos = 0; pos < len; ) {
          const take = Math.min(blockLen - this.pos, len - pos);
          for (let i = 0; i < take; i++)
            state[this.pos++] ^= data[pos++];
          if (this.pos === blockLen)
            this.keccak();
        }
        return this;
      }
      finish() {
        if (this.finished)
          return;
        this.finished = true;
        const { state, suffix, pos, blockLen } = this;
        state[pos] ^= suffix;
        if ((suffix & 128) !== 0 && pos === blockLen - 1)
          this.keccak();
        state[blockLen - 1] ^= 128;
        this.keccak();
      }
      writeInto(out) {
        (0, utils_ts_1.aexists)(this, false);
        (0, utils_ts_1.abytes)(out);
        this.finish();
        const bufferOut = this.state;
        const { blockLen } = this;
        for (let pos = 0, len = out.length; pos < len; ) {
          if (this.posOut >= blockLen)
            this.keccak();
          const take = Math.min(blockLen - this.posOut, len - pos);
          out.set(bufferOut.subarray(this.posOut, this.posOut + take), pos);
          this.posOut += take;
          pos += take;
        }
        return out;
      }
      xofInto(out) {
        if (!this.enableXOF)
          throw new Error("XOF is not possible for this instance");
        return this.writeInto(out);
      }
      xof(bytes) {
        (0, utils_ts_1.anumber)(bytes);
        return this.xofInto(new Uint8Array(bytes));
      }
      digestInto(out) {
        (0, utils_ts_1.aoutput)(out, this);
        if (this.finished)
          throw new Error("digest() was already called");
        this.writeInto(out);
        this.destroy();
        return out;
      }
      digest() {
        return this.digestInto(new Uint8Array(this.outputLen));
      }
      destroy() {
        this.destroyed = true;
        (0, utils_ts_1.clean)(this.state);
      }
      _cloneInto(to) {
        const { blockLen, suffix, outputLen, rounds, enableXOF } = this;
        to || (to = new _Keccak(blockLen, suffix, outputLen, enableXOF, rounds));
        to.state32.set(this.state32);
        to.pos = this.pos;
        to.posOut = this.posOut;
        to.finished = this.finished;
        to.rounds = rounds;
        to.suffix = suffix;
        to.outputLen = outputLen;
        to.enableXOF = enableXOF;
        to.destroyed = this.destroyed;
        return to;
      }
    };
    exports.Keccak = Keccak;
    var gen = (suffix, blockLen, outputLen) => (0, utils_ts_1.createHasher)(() => new Keccak(blockLen, suffix, outputLen));
    exports.sha3_224 = (() => gen(6, 144, 224 / 8))();
    exports.sha3_256 = (() => gen(6, 136, 256 / 8))();
    exports.sha3_384 = (() => gen(6, 104, 384 / 8))();
    exports.sha3_512 = (() => gen(6, 72, 512 / 8))();
    exports.keccak_224 = (() => gen(1, 144, 224 / 8))();
    exports.keccak_256 = (() => gen(1, 136, 256 / 8))();
    exports.keccak_384 = (() => gen(1, 104, 384 / 8))();
    exports.keccak_512 = (() => gen(1, 72, 512 / 8))();
    var genShake = (suffix, blockLen, outputLen) => (0, utils_ts_1.createXOFer)((opts = {}) => new Keccak(blockLen, suffix, opts.dkLen === void 0 ? outputLen : opts.dkLen, true));
    exports.shake128 = (() => genShake(31, 168, 128 / 8))();
    exports.shake256 = (() => genShake(31, 136, 256 / 8))();
  }
});

// pinned:evidence/tas/source/src/core/errors.ts
var TasError = class extends Error {
  code;
  details;
  constructor(code, message, details) {
    super(message);
    this.name = "TasError";
    this.code = code;
    this.details = details;
  }
};

// pinned:evidence/tas/source/src/core/workflow/sourceGate.ts
function verificationRequired() {
  throw new TasError(
    "WORKFLOW_SOURCE_VERIFICATION_REQUIRED",
    "The current Workflow source must be verified before this operation can run."
  );
}
function sameContext(left, right) {
  return left.fingerprint === right.fingerprint && left.chainId === right.chainId && left.rpcUrl === right.rpcUrl && left.workflowAddress.toLowerCase() === right.workflowAddress.toLowerCase();
}
function snapshot(context) {
  if (context.blockSelector.kind !== "block_hash") {
    return verificationRequired();
  }
  return Object.freeze({
    chainId: context.chainId,
    rpcUrl: context.rpcUrl,
    workflowAddress: context.workflowAddress,
    blockSelector: Object.freeze({ ...context.blockSelector }),
    fingerprint: context.fingerprint
  });
}
function createWorkflowSourceGate(options) {
  const resolveCurrent = options.resolveCurrent;
  let accepted;
  let revision = 0;
  return Object.freeze({
    accept(context) {
      accepted = snapshot(context);
      revision += 1;
    },
    assertAccepted(context) {
      const expected = accepted;
      if (expected === void 0) return verificationRequired();
      const selected = snapshot(context);
      if (!sameContext(expected, selected)) {
        accepted = void 0;
        revision += 1;
        return verificationRequired();
      }
      return selected;
    },
    invalidate() {
      accepted = void 0;
      revision += 1;
    },
    async assertCurrent(signal) {
      const expected = accepted;
      const expectedRevision = revision;
      if (expected === void 0) return verificationRequired();
      const current = snapshot(await resolveCurrent(signal));
      if (revision !== expectedRevision || accepted !== expected) return verificationRequired();
      if (!sameContext(expected, current)) {
        accepted = void 0;
        revision += 1;
        return verificationRequired();
      }
      return current;
    }
  });
}

// pinned:evidence/tas/source/src/core/workflow/operationService.ts
import { isProxy as isProxy2 } from "node:util/types";

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/errors/version.js
var version = "2.55.19";

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/errors/base.js
var errorConfig = {
  getDocsUrl: ({ docsBaseUrl, docsPath = "", docsSlug }) => docsPath ? `${docsBaseUrl ?? "https://viem.sh"}${docsPath}${docsSlug ? `#${docsSlug}` : ""}` : void 0,
  version: `viem@${version}`
};
var BaseError = class _BaseError extends Error {
  constructor(shortMessage, args = {}) {
    const details = (() => {
      if (args.cause instanceof _BaseError)
        return args.cause.details;
      if (args.cause?.message)
        return args.cause.message;
      return args.details;
    })();
    const docsPath = (() => {
      if (args.cause instanceof _BaseError)
        return args.cause.docsPath || args.docsPath;
      return args.docsPath;
    })();
    const docsUrl = errorConfig.getDocsUrl?.({ ...args, docsPath });
    const message = [
      shortMessage || "An error occurred.",
      "",
      ...args.metaMessages ? [...args.metaMessages, ""] : [],
      ...docsUrl ? [`Docs: ${docsUrl}`] : [],
      ...details ? [`Details: ${details}`] : [],
      ...errorConfig.version ? [`Version: ${errorConfig.version}`] : []
    ].join("\n");
    super(message, args.cause ? { cause: args.cause } : void 0);
    Object.defineProperty(this, "details", {
      enumerable: true,
      configurable: true,
      writable: true,
      value: void 0
    });
    Object.defineProperty(this, "docsPath", {
      enumerable: true,
      configurable: true,
      writable: true,
      value: void 0
    });
    Object.defineProperty(this, "metaMessages", {
      enumerable: true,
      configurable: true,
      writable: true,
      value: void 0
    });
    Object.defineProperty(this, "shortMessage", {
      enumerable: true,
      configurable: true,
      writable: true,
      value: void 0
    });
    Object.defineProperty(this, "version", {
      enumerable: true,
      configurable: true,
      writable: true,
      value: void 0
    });
    Object.defineProperty(this, "name", {
      enumerable: true,
      configurable: true,
      writable: true,
      value: "BaseError"
    });
    this.details = details;
    this.docsPath = docsPath;
    this.metaMessages = args.metaMessages;
    this.name = args.name ?? this.name;
    this.shortMessage = shortMessage;
    this.version = version;
  }
  walk(fn) {
    return walk(this, fn);
  }
};
function walk(err, fn) {
  if (fn?.(err))
    return err;
  if (err && typeof err === "object" && "cause" in err && err.cause !== void 0)
    return walk(err.cause, fn);
  return fn ? null : err;
}

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/errors/address.js
var InvalidAddressError = class extends BaseError {
  constructor({ address }) {
    super(`Address "${address}" is invalid.`, {
      metaMessages: [
        "- Address must be a hex value of 20 bytes (40 hex characters).",
        "- Address must match its checksum counterpart."
      ],
      name: "InvalidAddressError"
    });
  }
};

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/utils/data/isHex.js
function isHex(value, { strict = true } = {}) {
  if (!value)
    return false;
  if (typeof value !== "string")
    return false;
  return strict ? /^0x[0-9a-fA-F]*$/.test(value) : value.startsWith("0x");
}

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/errors/data.js
var SizeExceedsPaddingSizeError = class extends BaseError {
  constructor({ size: size2, targetSize, type }) {
    super(`${type.charAt(0).toUpperCase()}${type.slice(1).toLowerCase()} size (${size2}) exceeds padding size (${targetSize}).`, { name: "SizeExceedsPaddingSizeError" });
  }
};

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/utils/data/pad.js
function pad(hexOrBytes, { dir, size: size2 = 32 } = {}) {
  if (typeof hexOrBytes === "string")
    return padHex(hexOrBytes, { dir, size: size2 });
  return padBytes(hexOrBytes, { dir, size: size2 });
}
function padHex(hex_, { dir, size: size2 = 32 } = {}) {
  if (size2 === null)
    return hex_;
  const hex = hex_.replace("0x", "");
  if (hex.length > size2 * 2)
    throw new SizeExceedsPaddingSizeError({
      size: Math.ceil(hex.length / 2),
      targetSize: size2,
      type: "hex"
    });
  return `0x${hex[dir === "right" ? "padEnd" : "padStart"](size2 * 2, "0")}`;
}
function padBytes(bytes, { dir, size: size2 = 32 } = {}) {
  if (size2 === null)
    return bytes;
  if (bytes.length > size2)
    throw new SizeExceedsPaddingSizeError({
      size: bytes.length,
      targetSize: size2,
      type: "bytes"
    });
  const paddedBytes = new Uint8Array(size2);
  for (let i = 0; i < size2; i++) {
    const padEnd = dir === "right";
    paddedBytes[padEnd ? i : size2 - i - 1] = bytes[padEnd ? i : bytes.length - i - 1];
  }
  return paddedBytes;
}

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/errors/encoding.js
var IntegerOutOfRangeError = class extends BaseError {
  constructor({ max, min, signed, size: size2, value }) {
    super(`Number "${value}" is not in safe ${size2 ? `${size2 * 8}-bit ${signed ? "signed" : "unsigned"} ` : ""}integer range ${max ? `(${min} to ${max})` : `(above ${min})`}`, { name: "IntegerOutOfRangeError" });
  }
};
var SizeOverflowError = class extends BaseError {
  constructor({ givenSize, maxSize }) {
    super(`Size cannot exceed ${maxSize} bytes. Given size: ${givenSize} bytes.`, { name: "SizeOverflowError" });
  }
};

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/utils/data/size.js
function size(value) {
  if (isHex(value, { strict: false }))
    return Math.ceil((value.length - 2) / 2);
  return value.length;
}

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/utils/encoding/fromHex.js
function assertSize(hexOrBytes, { size: size2 }) {
  if (size(hexOrBytes) > size2)
    throw new SizeOverflowError({
      givenSize: size(hexOrBytes),
      maxSize: size2
    });
}

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/utils/encoding/toHex.js
var hexes = /* @__PURE__ */ Array.from({ length: 256 }, (_v, i) => i.toString(16).padStart(2, "0"));
function toHex(value, opts = {}) {
  if (typeof value === "number" || typeof value === "bigint")
    return numberToHex(value, opts);
  if (typeof value === "string") {
    return stringToHex(value, opts);
  }
  if (typeof value === "boolean")
    return boolToHex(value, opts);
  return bytesToHex(value, opts);
}
function boolToHex(value, opts = {}) {
  const hex = `0x${Number(value)}`;
  if (typeof opts.size === "number") {
    assertSize(hex, { size: opts.size });
    return pad(hex, { size: opts.size });
  }
  return hex;
}
function bytesToHex(value, opts = {}) {
  let string = "";
  for (let i = 0; i < value.length; i++) {
    string += hexes[value[i]];
  }
  const hex = `0x${string}`;
  if (typeof opts.size === "number") {
    assertSize(hex, { size: opts.size });
    return pad(hex, { dir: "right", size: opts.size });
  }
  return hex;
}
function numberToHex(value_, opts = {}) {
  const { signed, size: size2 } = opts;
  const value = BigInt(value_);
  let maxValue;
  if (size2) {
    if (signed)
      maxValue = (1n << BigInt(size2) * 8n - 1n) - 1n;
    else
      maxValue = 2n ** (BigInt(size2) * 8n) - 1n;
  } else if (typeof value_ === "number") {
    maxValue = BigInt(Number.MAX_SAFE_INTEGER);
  }
  const minValue = typeof maxValue === "bigint" && signed ? -maxValue - 1n : 0;
  if (maxValue && value > maxValue || value < minValue) {
    const suffix = typeof value_ === "bigint" ? "n" : "";
    throw new IntegerOutOfRangeError({
      max: maxValue ? `${maxValue}${suffix}` : void 0,
      min: `${minValue}${suffix}`,
      signed,
      size: size2,
      value: `${value_}${suffix}`
    });
  }
  const hex = `0x${(signed && value < 0 ? (1n << BigInt(size2 * 8)) + BigInt(value) : value).toString(16)}`;
  if (size2)
    return pad(hex, { size: size2 });
  return hex;
}
var encoder = /* @__PURE__ */ new TextEncoder();
function stringToHex(value_, opts = {}) {
  const value = encoder.encode(value_);
  return bytesToHex(value, opts);
}

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/utils/encoding/toBytes.js
var encoder2 = /* @__PURE__ */ new TextEncoder();
function toBytes(value, opts = {}) {
  if (typeof value === "number" || typeof value === "bigint")
    return numberToBytes(value, opts);
  if (typeof value === "boolean")
    return boolToBytes(value, opts);
  if (isHex(value))
    return hexToBytes(value, opts);
  return stringToBytes(value, opts);
}
function boolToBytes(value, opts = {}) {
  const bytes = new Uint8Array(1);
  bytes[0] = Number(value);
  if (typeof opts.size === "number") {
    assertSize(bytes, { size: opts.size });
    return pad(bytes, { size: opts.size });
  }
  return bytes;
}
var charCodeMap = {
  zero: 48,
  nine: 57,
  A: 65,
  F: 70,
  a: 97,
  f: 102
};
function charCodeToBase16(char) {
  if (char >= charCodeMap.zero && char <= charCodeMap.nine)
    return char - charCodeMap.zero;
  if (char >= charCodeMap.A && char <= charCodeMap.F)
    return char - (charCodeMap.A - 10);
  if (char >= charCodeMap.a && char <= charCodeMap.f)
    return char - (charCodeMap.a - 10);
  return void 0;
}
function hexToBytes(hex_, opts = {}) {
  let hex = hex_;
  if (opts.size) {
    assertSize(hex, { size: opts.size });
    hex = pad(hex, { dir: "right", size: opts.size });
  }
  let hexString2 = hex.slice(2);
  if (hexString2.length % 2)
    hexString2 = `0${hexString2}`;
  const length = hexString2.length / 2;
  const bytes = new Uint8Array(length);
  for (let index = 0, j = 0; index < length; index++) {
    const nibbleLeft = charCodeToBase16(hexString2.charCodeAt(j++));
    const nibbleRight = charCodeToBase16(hexString2.charCodeAt(j++));
    if (nibbleLeft === void 0 || nibbleRight === void 0) {
      throw new BaseError(`Invalid byte sequence ("${hexString2[j - 2]}${hexString2[j - 1]}" in "${hexString2}").`);
    }
    bytes[index] = nibbleLeft * 16 + nibbleRight;
  }
  return bytes;
}
function numberToBytes(value, opts) {
  const hex = numberToHex(value, opts);
  return hexToBytes(hex);
}
function stringToBytes(value, opts = {}) {
  const bytes = encoder2.encode(value);
  if (typeof opts.size === "number") {
    assertSize(bytes, { size: opts.size });
    return pad(bytes, { dir: "right", size: opts.size });
  }
  return bytes;
}

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/utils/hash/keccak256.js
var import_sha3 = __toESM(require_sha3());
function keccak256(value, to_) {
  const to = to_ || "hex";
  const bytes = (0, import_sha3.keccak_256)(isHex(value, { strict: false }) ? toBytes(value) : value);
  if (to === "bytes")
    return bytes;
  return toHex(bytes);
}

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/utils/lru.js
var LruMap = class extends Map {
  constructor(size2) {
    super();
    Object.defineProperty(this, "maxSize", {
      enumerable: true,
      configurable: true,
      writable: true,
      value: void 0
    });
    this.maxSize = size2;
  }
  get(key) {
    const value = super.get(key);
    if (super.has(key)) {
      super.delete(key);
      super.set(key, value);
    }
    return value;
  }
  set(key, value) {
    if (super.has(key))
      super.delete(key);
    super.set(key, value);
    if (this.maxSize && this.size > this.maxSize) {
      const firstKey = super.keys().next().value;
      if (firstKey !== void 0)
        super.delete(firstKey);
    }
    return this;
  }
};

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/utils/address/isAddress.js
var addressRegex = /^0x[a-fA-F0-9]{40}$/;
var isAddressCache = /* @__PURE__ */ new LruMap(8192);
function isAddress(address, options) {
  const { strict = true } = options ?? {};
  const cacheKey = `${address}.${strict}`;
  if (isAddressCache.has(cacheKey))
    return isAddressCache.get(cacheKey);
  const result = (() => {
    if (!addressRegex.test(address))
      return false;
    if (address.toLowerCase() === address)
      return true;
    if (strict)
      return checksumAddress(address) === address;
    return true;
  })();
  isAddressCache.set(cacheKey, result);
  return result;
}

// pinned:artifacts/tas-phase3a/runtime/node_modules/viem/_esm/utils/address/getAddress.js
var checksumAddressCache = /* @__PURE__ */ new LruMap(8192);
function checksumAddress(address_, chainId) {
  if (checksumAddressCache.has(`${address_}.${chainId}`))
    return checksumAddressCache.get(`${address_}.${chainId}`);
  const hexAddress = chainId ? `${chainId}${address_.toLowerCase()}` : address_.substring(2).toLowerCase();
  const hash = keccak256(stringToBytes(hexAddress), "bytes");
  const address = (chainId ? hexAddress.substring(`${chainId}0x`.length) : hexAddress).split("");
  for (let i = 0; i < 40; i += 2) {
    if (hash[i >> 1] >> 4 >= 8 && address[i]) {
      address[i] = address[i].toUpperCase();
    }
    if ((hash[i >> 1] & 15) >= 8 && address[i + 1]) {
      address[i + 1] = address[i + 1].toUpperCase();
    }
  }
  const result = `0x${address.join("")}`;
  checksumAddressCache.set(`${address_}.${chainId}`, result);
  return result;
}
function getAddress(address, chainId) {
  if (!isAddress(address, { strict: false }))
    throw new InvalidAddressError({ address });
  return checksumAddress(address, chainId);
}

// pinned:evidence/tas/source/src/clients/chain/jsonCodec.ts
import { isProxy } from "node:util/types";
var maximumDepth = 64;
var maximumNodes = 1e4;
var maximumBytes = 1024 * 1024;
var maximumUnionMembers = 256;
var arrayIndex = /^(?:0|[1-9][0-9]*)$/;
var canonicalInteger = /^(?:0|-?[1-9][0-9]*)$/;
var canonicalUnsignedInteger = /^(?:0|[1-9][0-9]*)$/;
var hexString = /^0x[0-9a-fA-F]*$/;
var evmAddress = /^0x[0-9a-fA-F]{40}$/;
var supportedPatterns = /* @__PURE__ */ new Map([
  ["^(?:0|-?[1-9][0-9]*)$", /^(?:0|-?[1-9][0-9]*)$/],
  ["^(?:0|[1-9][0-9]*)$", /^(?:0|[1-9][0-9]*)$/],
  ["^0x[0-9a-f]+$", /^0x[0-9a-f]+$/]
]);
var supportedSchemaKeys = /* @__PURE__ */ new Set([
  "$defs",
  "$ref",
  "$schema",
  "additionalProperties",
  "anyOf",
  "const",
  "enum",
  "format",
  "items",
  "maxItems",
  "maxLength",
  "minItems",
  "minLength",
  "oneOf",
  "pattern",
  "prefixItems",
  "properties",
  "required",
  "type",
  "writeOnly",
  "x-tas-type"
]);
var ValueMismatch = class extends Error {
};
var FatalCodecError = class extends Error {
};
function charge(budget, bytes = 0, nodes = 1) {
  budget.nodes += nodes;
  budget.bytes += bytes;
  if (budget.nodes > maximumNodes) throw new FatalCodecError(`EVM JSON work exceeds ${maximumNodes} nodes`);
  if (budget.bytes > maximumBytes) throw new FatalCodecError(`EVM JSON data exceeds ${maximumBytes} bytes`);
}
function stringBytes(value) {
  return Buffer.byteLength(value, "utf8");
}
function ownDescriptors(value, label, budget) {
  if (isProxy(value)) throw new FatalCodecError(`${label} must not be a Proxy`);
  if (Object.getOwnPropertySymbols(value).length > 0) throw new FatalCodecError(`${label} must use string keys`);
  const descriptors = Object.getOwnPropertyDescriptors(value);
  for (const key of Object.keys(descriptors)) charge(budget, stringBytes(key), 0);
  return descriptors;
}
function plainObjectDescriptors(value, label, budget) {
  const prototype = Object.getPrototypeOf(value);
  if (prototype !== Object.prototype && prototype !== null) throw new FatalCodecError(`${label} must be a plain object`);
  const descriptors = ownDescriptors(value, label, budget);
  for (const key of Object.keys(descriptors)) {
    const descriptor = descriptors[key];
    if (descriptor === void 0 || !descriptor.enumerable || !("value" in descriptor)) {
      throw new FatalCodecError(`${label}.${key} must be an enumerable data property`);
    }
  }
  return descriptors;
}
function arrayDescriptors(value, label, budget) {
  if (isProxy(value)) throw new FatalCodecError(`${label} must not be a Proxy`);
  const prototype = Object.getPrototypeOf(value);
  if (prototype !== Array.prototype && prototype !== null) throw new FatalCodecError(`${label} has an unsupported array prototype`);
  const lengthDescriptor = Object.getOwnPropertyDescriptor(value, "length");
  if (lengthDescriptor === void 0 || !("value" in lengthDescriptor) || typeof lengthDescriptor.value !== "number" || !Number.isSafeInteger(lengthDescriptor.value) || lengthDescriptor.value < 0) throw new FatalCodecError(`${label} has an invalid length`);
  const length = lengthDescriptor.value;
  if (budget.nodes + length > maximumNodes) throw new FatalCodecError(`${label} exceeds the work budget`);
  const descriptors = ownDescriptors(value, label, budget);
  let entries = 0;
  for (const key of Object.keys(descriptors)) {
    if (key === "length") continue;
    const descriptor = descriptors[key];
    if (!arrayIndex.test(key) || Number(key) >= length || descriptor === void 0 || !descriptor.enumerable || !("value" in descriptor)) {
      throw new FatalCodecError(`${label} must contain only dense enumerable index properties`);
    }
    entries += 1;
  }
  if (entries !== length) throw new FatalCodecError(`${label} must not be sparse`);
  return { descriptors, length };
}
var typedArrayPrototype = Object.getPrototypeOf(Uint8Array.prototype);
var typedArrayBufferGetter = Object.getOwnPropertyDescriptor(typedArrayPrototype, "buffer")?.get;
var typedArrayByteLengthGetter = Object.getOwnPropertyDescriptor(typedArrayPrototype, "byteLength")?.get;
var typedArrayByteOffsetGetter = Object.getOwnPropertyDescriptor(typedArrayPrototype, "byteOffset")?.get;
function encodeBytes(value, budget) {
  if (isProxy(value) || Object.getPrototypeOf(value) !== Uint8Array.prototype) {
    throw new FatalCodecError("bytes must be a direct built-in Uint8Array");
  }
  if (typedArrayBufferGetter === void 0 || typedArrayByteLengthGetter === void 0 || typedArrayByteOffsetGetter === void 0) {
    throw new FatalCodecError("built-in Uint8Array accessors are unavailable");
  }
  const byteLength = typedArrayByteLengthGetter.call(value);
  if (typeof byteLength !== "number" || !Number.isSafeInteger(byteLength) || byteLength < 0) {
    throw new FatalCodecError("bytes have invalid built-in storage");
  }
  charge(budget, byteLength * 2 + 2 + stringBytes("encodingvaluehex"), byteLength + 3);
  const descriptors = ownDescriptors(value, "bytes", budget);
  for (const key of Object.keys(descriptors)) {
    const descriptor = descriptors[key];
    if (!arrayIndex.test(key) || descriptor === void 0 || !descriptor.enumerable || !("value" in descriptor)) {
      throw new FatalCodecError("bytes must not override built-in properties");
    }
  }
  const byteOffset = typedArrayByteOffsetGetter.call(value);
  const buffer = typedArrayBufferGetter.call(value);
  if (typeof byteOffset !== "number" || !(buffer instanceof ArrayBuffer)) throw new FatalCodecError("bytes have invalid built-in storage");
  return { encoding: "hex", value: `0x${Buffer.from(buffer, byteOffset, byteLength).toString("hex")}` };
}
function encode(value, state, depth) {
  if (depth > maximumDepth) throw new FatalCodecError(`EVM JSON depth exceeds ${maximumDepth}`);
  if (value === null || typeof value === "boolean") {
    charge(state.budget);
    return value;
  }
  if (typeof value === "string") {
    charge(state.budget, stringBytes(value));
    return value;
  }
  if (typeof value === "bigint") {
    const encoded = value.toString(10);
    if (encoded.length > 79) throw new FatalCodecError("EVM JSON bigint exceeds 79 canonical characters");
    charge(state.budget, stringBytes(encoded));
    return encoded;
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value) || Object.is(value, -0) || Number.isInteger(value) && !Number.isSafeInteger(value)) {
      throw new FatalCodecError("EVM JSON numbers must be finite, safe, and not negative zero");
    }
    charge(state.budget);
    return value;
  }
  if (typeof value !== "object") throw new FatalCodecError(`unsupported EVM JSON value: ${typeof value}`);
  if (isProxy(value)) throw new FatalCodecError("EVM JSON values must not be Proxies");
  if (value instanceof Uint8Array) return encodeBytes(value, state.budget);
  if (state.active.has(value)) throw new FatalCodecError("EVM JSON graph contains a cycle");
  charge(state.budget);
  state.active.add(value);
  try {
    if (Array.isArray(value)) {
      const { descriptors: descriptors2, length } = arrayDescriptors(value, "EVM JSON array", state.budget);
      const result2 = [];
      for (let index = 0; index < length; index += 1) {
        const descriptor = descriptors2[String(index)];
        if (descriptor === void 0 || !("value" in descriptor)) throw new FatalCodecError("EVM JSON array is sparse");
        result2.push(encode(descriptor.value, state, depth + 1));
      }
      return result2;
    }
    const descriptors = plainObjectDescriptors(value, "EVM JSON object", state.budget);
    const keys = Object.keys(descriptors).sort();
    if (state.budget.nodes + keys.length > maximumNodes) throw new FatalCodecError("EVM JSON object exceeds the work budget");
    const result = /* @__PURE__ */ Object.create(null);
    for (const key of keys) {
      const descriptor = descriptors[key];
      if (descriptor === void 0 || !("value" in descriptor)) throw new FatalCodecError(`unresolved EVM JSON property ${key}`);
      result[key] = encode(descriptor.value, state, depth + 1);
    }
    return result;
  } finally {
    state.active.delete(value);
  }
}
function encodeEvmJson(value) {
  return encode(value, { budget: { nodes: 0, bytes: 0 }, active: /* @__PURE__ */ new Set(), references: /* @__PURE__ */ new Map() }, 0);
}
function cloneSchema(value, budget, active = /* @__PURE__ */ new Set(), depth = 0) {
  if (depth > maximumDepth) throw new FatalCodecError(`schema depth exceeds ${maximumDepth}`);
  if (value === null || typeof value === "boolean") {
    charge(budget);
    return value;
  }
  if (typeof value === "string") {
    charge(budget, stringBytes(value));
    return value;
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value) || Object.is(value, -0)) throw new FatalCodecError("schema number is invalid");
    charge(budget);
    return value;
  }
  if (typeof value !== "object" || isProxy(value)) throw new FatalCodecError("schema must be plain JSON");
  if (active.has(value)) throw new FatalCodecError("schema must not contain cycles");
  charge(budget);
  active.add(value);
  try {
    if (Array.isArray(value)) {
      const { descriptors: descriptors2, length } = arrayDescriptors(value, "schema array", budget);
      const result2 = [];
      for (let index = 0; index < length; index += 1) {
        const descriptor = descriptors2[String(index)];
        if (descriptor === void 0 || !("value" in descriptor)) throw new FatalCodecError("schema array is sparse");
        result2.push(cloneSchema(descriptor.value, budget, active, depth + 1));
      }
      return result2;
    }
    const descriptors = plainObjectDescriptors(value, "schema object", budget);
    const keys = Object.keys(descriptors).sort();
    if (budget.nodes + keys.length > maximumNodes) throw new FatalCodecError("schema object exceeds the work budget");
    const result = /* @__PURE__ */ Object.create(null);
    for (const key of keys) {
      const descriptor = descriptors[key];
      if (descriptor === void 0 || !("value" in descriptor)) throw new FatalCodecError(`unresolved schema property ${key}`);
      result[key] = cloneSchema(descriptor.value, budget, active, depth + 1);
    }
    return result;
  } finally {
    active.delete(value);
  }
}
function asRecord(value, label) {
  if (typeof value !== "object" || value === null || Array.isArray(value)) throw new FatalCodecError(`${label} must be an object`);
  return value;
}
function asArray(value, label) {
  if (!Array.isArray(value)) throw new FatalCodecError(`${label} must be an array`);
  return value;
}
function own(schema, key) {
  return Object.prototype.hasOwnProperty.call(schema, key) ? schema[key] : void 0;
}
function validateScalarConstraints(schema) {
  const constant = own(schema, "const");
  const enumeration = own(schema, "enum");
  if (constant !== void 0 && enumeration !== void 0) throw new FatalCodecError("schema cannot combine const and enum");
  for (const [keyword, value] of [["const", constant], ["enum", enumeration]]) {
    if (value === void 0) continue;
    const values = keyword === "enum" ? asArray(value, "schema enum") : [value];
    if (values.length === 0 || values.length > maximumUnionMembers) {
      throw new FatalCodecError(`schema ${keyword} has an unsupported number of values`);
    }
    for (let index = 0; index < values.length; index += 1) {
      const candidate = values[index];
      if (candidate !== null && typeof candidate === "object") throw new FatalCodecError(`${keyword} supports scalar values only`);
    }
  }
}
function validateBytesMarker(schema, properties, required) {
  if (own(schema, "x-tas-type") !== "bytes") throw new FatalCodecError("unsupported x-tas-type marker");
  if (own(schema, "type") !== "object" || own(schema, "additionalProperties") !== false) {
    throw new FatalCodecError("bytes schema must be a closed object");
  }
  if (Object.keys(properties).toSorted().join("\0") !== "encoding\0value" || [...required].toSorted().join("\0") !== "encoding\0value") {
    throw new FatalCodecError("bytes schema must contain exactly encoding and value");
  }
  const encoding = asRecord(properties.encoding, "bytes encoding schema");
  const value = asRecord(properties.value, "bytes value schema");
  const outerKeys = Object.keys(schema).filter((key) => key !== "$schema" && key !== "$defs").toSorted();
  if (outerKeys.join("\0") !== "additionalProperties\0properties\0required\0type\0x-tas-type" || Object.keys(encoding).toSorted().join("\0") !== "const\0type" || Object.keys(value).toSorted().join("\0") !== "format\0type" || own(encoding, "type") !== "string" || own(encoding, "const") !== "hex" || own(value, "type") !== "string" || own(value, "format") !== "hex") {
    throw new FatalCodecError("bytes schema has an invalid binary envelope");
  }
}
function validateSchema(schema, root, active = /* @__PURE__ */ new Set()) {
  if (active.has(schema)) throw new FatalCodecError("schema structure is recursive");
  active.add(schema);
  try {
    for (const key of Object.keys(schema)) {
      if (!supportedSchemaKeys.has(key)) throw new FatalCodecError(`unsupported schema keyword ${key}`);
    }
    const reference = own(schema, "$ref");
    if (reference !== void 0) {
      if (typeof reference !== "string" || !reference.startsWith("#/$defs/")) throw new FatalCodecError("only local $defs references are supported");
      const siblings = Object.keys(schema).filter((key) => key !== "$ref" && key !== "$defs" && key !== "$schema");
      if (siblings.length > 0) throw new FatalCodecError("$ref siblings are not supported");
    }
    const schemaVersion = own(schema, "$schema");
    if (schemaVersion !== void 0 && schemaVersion !== "https://json-schema.org/draft/2020-12/schema") {
      throw new FatalCodecError("unsupported JSON Schema version");
    }
    const type = own(schema, "type");
    if (type !== void 0 && (typeof type !== "string" || !["null", "boolean", "number", "string", "array", "object"].includes(type))) {
      throw new FatalCodecError("unsupported schema type");
    }
    const format = own(schema, "format");
    if (format !== void 0 && (typeof format !== "string" || !["bigint", "uint256", "int256", "hex", "evm-address"].includes(format))) {
      throw new FatalCodecError("unsupported schema format");
    }
    const pattern = own(schema, "pattern");
    if (pattern !== void 0) {
      if (typeof pattern !== "string") throw new FatalCodecError("schema pattern must be a string");
      if (!supportedPatterns.has(pattern)) throw new FatalCodecError("schema pattern is not in the supported deterministic set");
    }
    for (const keyword of ["minLength", "maxLength"]) {
      const length = own(schema, keyword);
      if (length !== void 0 && (typeof length !== "number" || !Number.isSafeInteger(length) || length < 0)) {
        throw new FatalCodecError(`schema ${keyword} is invalid`);
      }
    }
    const writeOnly = own(schema, "writeOnly");
    if (writeOnly !== void 0 && typeof writeOnly !== "boolean") throw new FatalCodecError("schema writeOnly must be boolean");
    for (const keyword of ["minItems", "maxItems"]) {
      const value = own(schema, keyword);
      if (value !== void 0 && (typeof value !== "number" || !Number.isSafeInteger(value) || value < 0)) {
        throw new FatalCodecError(`schema ${keyword} is invalid`);
      }
    }
    validateScalarConstraints(schema);
    const required = own(schema, "required");
    let requiredNames = [];
    if (required !== void 0) {
      const entries = asArray(required, "schema required");
      const names = /* @__PURE__ */ new Set();
      for (let index = 0; index < entries.length; index += 1) {
        const name = entries[index];
        if (typeof name !== "string" || names.has(name)) throw new FatalCodecError("schema required must contain unique strings");
        names.add(name);
      }
      requiredNames = [...names];
    }
    const definitions = own(schema, "$defs");
    if (definitions !== void 0) {
      const record = asRecord(definitions, "schema $defs");
      for (const key of Object.keys(record)) validateSchema(asRecord(record[key], `schema definition ${key}`), root, active);
    }
    const properties = own(schema, "properties");
    if (properties !== void 0) {
      const record = asRecord(properties, "schema properties");
      for (const key of Object.keys(record)) validateSchema(asRecord(record[key], `schema property ${key}`), root, active);
    }
    const oneOf = own(schema, "oneOf");
    const anyOf = own(schema, "anyOf");
    const unionKeyword = oneOf !== void 0 ? "oneOf" : anyOf !== void 0 ? "anyOf" : void 0;
    if (unionKeyword !== void 0) {
      const siblings = Object.keys(schema).filter((key) => key !== unionKeyword && key !== "$defs" && key !== "$schema");
      if (siblings.length > 0) throw new FatalCodecError(`${unionKeyword} siblings are not supported`);
      const branches = asArray(own(schema, unionKeyword), `schema ${unionKeyword}`);
      if (branches.length === 0 || branches.length > maximumUnionMembers) {
        throw new FatalCodecError(`schema ${unionKeyword} must contain 1-${maximumUnionMembers} branches`);
      }
      for (let index = 0; index < branches.length; index += 1) validateSchema(asRecord(branches[index], "schema branch"), root, active);
      return;
    }
    const prefixItems = own(schema, "prefixItems");
    if (prefixItems !== void 0) {
      const entries = asArray(prefixItems, "schema prefixItems");
      for (let index = 0; index < entries.length; index += 1) validateSchema(asRecord(entries[index], "schema tuple item"), root, active);
    }
    for (const keyword of ["items", "additionalProperties"]) {
      const value = own(schema, keyword);
      if (value !== void 0 && typeof value !== "boolean") validateSchema(asRecord(value, `schema ${keyword}`), root, active);
      if (keyword === "items" && value === true) throw new FatalCodecError("schema items=true is unsupported");
    }
    if (reference !== void 0) return;
    if (type === void 0) {
      if (own(schema, "const") === void 0 && own(schema, "enum") === void 0) {
        throw new FatalCodecError("schema must define type, oneOf, anyOf, $ref, const, or enum");
      }
      return;
    }
    const minLength = own(schema, "minLength");
    const maxLength = own(schema, "maxLength");
    const stringKeywords = format !== void 0 || pattern !== void 0 || minLength !== void 0 || maxLength !== void 0 || writeOnly !== void 0;
    if (stringKeywords && type !== "string") throw new FatalCodecError("string keyword requires type=string");
    if (typeof minLength === "number" && typeof maxLength === "number" && minLength > maxLength) {
      throw new FatalCodecError("schema minLength exceeds maxLength");
    }
    const arrayKeywords = ["items", "prefixItems", "minItems", "maxItems"].some((key) => own(schema, key) !== void 0);
    if (arrayKeywords && type !== "array") throw new FatalCodecError("array keyword requires type=array");
    const objectKeywords = ["properties", "required", "additionalProperties", "x-tas-type"].some((key) => own(schema, key) !== void 0);
    if (objectKeywords && type !== "object") throw new FatalCodecError("object keyword requires type=object");
    const minimum = own(schema, "minItems");
    const maximum = own(schema, "maxItems");
    if (typeof minimum === "number" && typeof maximum === "number" && minimum > maximum) {
      throw new FatalCodecError("schema minItems exceeds maxItems");
    }
    if (type === "object") {
      const propertyRecord = properties === void 0 ? /* @__PURE__ */ Object.create(null) : asRecord(properties, "schema properties");
      if (requiredNames.some((name) => !Object.hasOwn(propertyRecord, name))) {
        throw new FatalCodecError("schema required names must exist in properties");
      }
      if (own(schema, "x-tas-type") !== void 0) validateBytesMarker(schema, propertyRecord, requiredNames);
    }
  } finally {
    active.delete(schema);
  }
}
function resolveReference(reference, root) {
  const name = reference.slice("#/$defs/".length);
  if (name.length === 0 || name.includes("/") || name === "__proto__") throw new FatalCodecError("invalid local schema reference");
  const definitions = asRecord(own(root, "$defs"), "schema $defs");
  if (!Object.prototype.hasOwnProperty.call(definitions, name)) throw new FatalCodecError(`unresolved schema reference ${reference}`);
  return asRecord(definitions[name], `schema definition ${name}`);
}
function mismatch(message) {
  throw new ValueMismatch(message);
}
function decodeInteger(format, value) {
  if (typeof value !== "string") return mismatch(`${format} must be a canonical decimal string`);
  const pattern = format === "uint256" ? canonicalUnsignedInteger : canonicalInteger;
  if (!pattern.test(value)) return mismatch(`${format} must be a canonical decimal string`);
  const maximumDigits = format === "bigint" ? 79 : 78;
  if (value.length > maximumDigits) return mismatch(`${format} exceeds the supported decimal width`);
  const decoded = BigInt(value);
  if (format === "uint256" && (decoded < 0n || decoded >= 2n ** 256n)) return mismatch("uint256 is out of range");
  if (format === "int256" && (decoded < -(2n ** 255n) || decoded >= 2n ** 255n)) return mismatch("int256 is out of range");
  return decoded;
}
function dataProperty(value, key, label) {
  const descriptor = Object.getOwnPropertyDescriptor(value, key);
  if (descriptor === void 0 || !descriptor.enumerable || !("value" in descriptor)) {
    throw new FatalCodecError(`${label}.${key} must be an enumerable data property`);
  }
  return descriptor.value;
}
function decodeBytesEnvelope(value, state) {
  if (typeof value !== "object" || value === null || Array.isArray(value) || isProxy(value)) {
    return mismatch("bytes value must be a binary envelope");
  }
  const descriptors = plainObjectDescriptors(value, "bytes envelope", state.budget);
  const keys = Object.keys(descriptors).toSorted();
  if (keys.join("\0") !== "encoding\0value") return mismatch("bytes envelope has unexpected properties");
  const encoding = dataProperty(value, "encoding", "bytes envelope");
  const encoded = dataProperty(value, "value", "bytes envelope");
  if (encoding !== "hex" || typeof encoded !== "string" || !/^0x(?:[0-9a-fA-F]{2})*$/.test(encoded)) return mismatch("bytes envelope must contain even-length hex");
  charge(state.budget, stringBytes(encoding) + stringBytes(encoded), (encoded.length - 2) / 2);
  return Uint8Array.from(Buffer.from(encoded.slice(2), "hex"));
}
function decodedValuesEquivalent(left, right, budget, depth) {
  if (depth > maximumDepth) throw new FatalCodecError(`decoded comparison depth exceeds ${maximumDepth}`);
  charge(budget);
  if (left === null || right === null || typeof left !== "object" || typeof right !== "object") {
    return Object.is(left, right);
  }
  if (left instanceof Uint8Array || right instanceof Uint8Array) {
    if (!(left instanceof Uint8Array) || !(right instanceof Uint8Array) || Object.getPrototypeOf(left) !== Uint8Array.prototype || Object.getPrototypeOf(right) !== Uint8Array.prototype || typedArrayByteLengthGetter === void 0 || typedArrayByteOffsetGetter === void 0 || typedArrayBufferGetter === void 0) return false;
    const leftLength = typedArrayByteLengthGetter.call(left);
    const rightLength = typedArrayByteLengthGetter.call(right);
    if (leftLength !== rightLength) return false;
    charge(budget, 0, leftLength);
    const leftBuffer = typedArrayBufferGetter.call(left);
    const rightBuffer = typedArrayBufferGetter.call(right);
    const leftOffset = typedArrayByteOffsetGetter.call(left);
    const rightOffset = typedArrayByteOffsetGetter.call(right);
    return Buffer.from(leftBuffer, leftOffset, leftLength).equals(Buffer.from(rightBuffer, rightOffset, rightLength));
  }
  if (Array.isArray(left) || Array.isArray(right)) {
    if (!Array.isArray(left) || !Array.isArray(right)) return false;
    const leftArray = arrayDescriptors(left, "decoded comparison array", budget);
    const rightArray = arrayDescriptors(right, "decoded comparison array", budget);
    if (leftArray.length !== rightArray.length) return false;
    for (let index = 0; index < leftArray.length; index += 1) {
      const leftValue = leftArray.descriptors[String(index)];
      const rightValue = rightArray.descriptors[String(index)];
      if (leftValue === void 0 || rightValue === void 0 || !("value" in leftValue) || !("value" in rightValue) || !decodedValuesEquivalent(
        leftValue.value,
        rightValue.value,
        budget,
        depth + 1
      )) return false;
    }
    return true;
  }
  const leftDescriptors = plainObjectDescriptors(left, "decoded comparison object", budget);
  const rightDescriptors = plainObjectDescriptors(right, "decoded comparison object", budget);
  const leftKeys = Object.keys(leftDescriptors).toSorted();
  const rightKeys = Object.keys(rightDescriptors).toSorted();
  if (leftKeys.length !== rightKeys.length || leftKeys.some((key, index) => key !== rightKeys[index])) return false;
  for (const key of leftKeys) {
    const leftValue = leftDescriptors[key];
    const rightValue = rightDescriptors[key];
    if (leftValue === void 0 || rightValue === void 0 || !("value" in leftValue) || !("value" in rightValue) || !decodedValuesEquivalent(
      leftValue.value,
      rightValue.value,
      budget,
      depth + 1
    )) return false;
  }
  return true;
}
function decode(schema, value, root, state, depth) {
  if (depth > maximumDepth) throw new FatalCodecError(`decoded EVM JSON depth exceeds ${maximumDepth}`);
  charge(state.budget, typeof value === "string" ? stringBytes(value) : 0);
  const reference = own(schema, "$ref");
  if (typeof reference === "string") {
    const values = state.references.get(reference) ?? /* @__PURE__ */ new Set();
    if (values.has(value)) throw new FatalCodecError(`recursive schema reference ${reference}`);
    values.add(value);
    state.references.set(reference, values);
    try {
      return decode(resolveReference(reference, root), value, root, state, depth + 1);
    } finally {
      values.delete(value);
      if (values.size === 0) state.references.delete(reference);
    }
  }
  const constant = own(schema, "const");
  if (constant !== void 0 && value !== constant) return mismatch("value does not match schema const");
  const enumeration = own(schema, "enum");
  if (enumeration !== void 0) {
    const entries = asArray(enumeration, "schema enum");
    let found = false;
    for (let index = 0; index < entries.length; index += 1) if (entries[index] === value) found = true;
    if (!found) return mismatch("value does not match schema enum");
  }
  const oneOf = own(schema, "oneOf");
  if (oneOf !== void 0) {
    const branches = asArray(oneOf, "schema oneOf");
    if (branches.length > maximumUnionMembers) throw new FatalCodecError("schema oneOf exceeds the branch budget");
    charge(state.budget, 0, branches.length);
    let matched;
    let matches = 0;
    for (let index = 0; index < branches.length; index += 1) {
      try {
        const decoded = decode(asRecord(branches[index], "schema branch"), value, root, state, depth + 1);
        matches += 1;
        if (matches > 1) throw new FatalCodecError("value matches more than one schema branch");
        matched = decoded;
      } catch (error) {
        if (!(error instanceof ValueMismatch)) throw error;
      }
    }
    if (matches !== 1 || matched === void 0) return mismatch("value must match exactly one schema branch");
    return matched;
  }
  const anyOf = own(schema, "anyOf");
  if (anyOf !== void 0) {
    const branches = asArray(anyOf, "schema anyOf");
    if (branches.length > maximumUnionMembers) throw new FatalCodecError("schema anyOf exceeds the branch budget");
    charge(state.budget, 0, branches.length);
    let matched;
    let matches = 0;
    for (let index = 0; index < branches.length; index += 1) {
      try {
        const decoded = decode(asRecord(branches[index], "schema branch"), value, root, state, depth + 1);
        if (matches > 0 && matched !== void 0 && !decodedValuesEquivalent(matched, decoded, state.budget, depth + 1)) {
          throw new FatalCodecError("ambiguous anyOf branches decode the value differently");
        }
        matched = decoded;
        matches += 1;
      } catch (error) {
        if (!(error instanceof ValueMismatch)) throw error;
      }
    }
    if (matches === 0 || matched === void 0) return mismatch("value must match at least one schema branch");
    return matched;
  }
  const type = own(schema, "type");
  if (type === void 0 && (constant !== void 0 || enumeration !== void 0)) {
    if (value === null || typeof value === "boolean" || typeof value === "string" || typeof value === "number" && Number.isFinite(value) && !Object.is(value, -0)) return value;
    return mismatch("const/enum value is not a supported scalar");
  }
  if (type === "null") {
    if (value !== null) return mismatch("value must be null");
    return null;
  }
  if (type === "boolean") {
    if (typeof value !== "boolean") return mismatch("value must be boolean");
    return value;
  }
  if (type === "number") {
    if (typeof value !== "number" || !Number.isFinite(value) || Object.is(value, -0) || Number.isInteger(value) && !Number.isSafeInteger(value)) return mismatch("value must be a finite safe number");
    return value;
  }
  if (type === "string") {
    const format = own(schema, "format");
    let result;
    if (format === "bigint" || format === "uint256" || format === "int256") result = decodeInteger(format, value);
    else {
      if (typeof value !== "string") return mismatch("value must be string");
      if (format === "hex" && !hexString.test(value)) return mismatch("value must be 0x-prefixed hex");
      if (format === "evm-address" && !evmAddress.test(value)) return mismatch("value must be a 20-byte EVM address");
      result = value;
    }
    if (typeof value !== "string") return mismatch("value must be string");
    const minLength = own(schema, "minLength");
    if (typeof minLength === "number" && value.length < minLength) return mismatch("value is shorter than minLength");
    const maxLength = own(schema, "maxLength");
    if (typeof maxLength === "number" && value.length > maxLength) return mismatch("value is longer than maxLength");
    const pattern = own(schema, "pattern");
    if (typeof pattern === "string" && !(supportedPatterns.get(pattern)?.test(value) ?? false)) {
      return mismatch("value does not match schema pattern");
    }
    return result;
  }
  if (type === "array") {
    if (!Array.isArray(value) || isProxy(value)) return mismatch("value must be an array");
    if (state.active.has(value)) throw new FatalCodecError("decoded value contains a cycle");
    const { descriptors, length } = arrayDescriptors(value, "decoded array", state.budget);
    const minimum = own(schema, "minItems");
    const maximum = own(schema, "maxItems");
    if (typeof minimum === "number" && length < minimum) return mismatch("array is shorter than minItems");
    if (typeof maximum === "number" && length > maximum) return mismatch("array is longer than maxItems");
    state.active.add(value);
    try {
      const prefixItems = own(schema, "prefixItems");
      const prefix = prefixItems === void 0 ? void 0 : asArray(prefixItems, "schema prefixItems");
      const result = [];
      for (let index = 0; index < length; index += 1) {
        const itemSchema = prefix !== void 0 && index < prefix.length ? prefix[index] : own(schema, "items");
        if (itemSchema === false || itemSchema === void 0) return mismatch(`array item ${index} is not allowed`);
        result.push(decode(asRecord(itemSchema, "schema item"), dataProperty(value, String(index), "decoded array"), root, state, depth + 1));
      }
      return result;
    } finally {
      state.active.delete(value);
    }
  }
  if (type === "object") {
    if (own(schema, "x-tas-type") === "bytes") return decodeBytesEnvelope(value, state);
    if (typeof value !== "object" || value === null || Array.isArray(value) || isProxy(value)) return mismatch("value must be an object");
    if (state.active.has(value)) throw new FatalCodecError("decoded value contains a cycle");
    const descriptors = plainObjectDescriptors(value, "decoded object", state.budget);
    state.active.add(value);
    try {
      const propertiesValue = own(schema, "properties");
      const properties = propertiesValue === void 0 ? /* @__PURE__ */ Object.create(null) : asRecord(propertiesValue, "schema properties");
      const requiredValue = own(schema, "required");
      if (requiredValue !== void 0) {
        const required = asArray(requiredValue, "schema required");
        for (let index = 0; index < required.length; index += 1) {
          const key = required[index];
          if (typeof key !== "string" || !Object.prototype.hasOwnProperty.call(descriptors, key)) return mismatch(`missing required property ${String(key)}`);
        }
      }
      const additional = own(schema, "additionalProperties");
      const result = /* @__PURE__ */ Object.create(null);
      for (const key of Object.keys(descriptors).sort()) {
        const raw = dataProperty(value, key, "decoded object");
        if (Object.prototype.hasOwnProperty.call(properties, key)) {
          result[key] = decode(asRecord(properties[key], `schema property ${key}`), raw, root, state, depth + 1);
        } else if (additional === false || additional === void 0) return mismatch(`additional property ${key} is not allowed`);
        else if (additional === true) result[key] = decodeJson(raw, state, depth + 1);
        else result[key] = decode(asRecord(additional, "schema additionalProperties"), raw, root, state, depth + 1);
      }
      return result;
    } finally {
      state.active.delete(value);
    }
  }
  throw new FatalCodecError(`unsupported schema type ${String(type)}`);
}
function decodeJson(value, state, depth) {
  return encode(value, state, depth);
}
function decodeBySchema(schemaValue, value) {
  const schemaBudget = { nodes: 0, bytes: 0 };
  const root = asRecord(cloneSchema(schemaValue, schemaBudget), "root schema");
  validateSchema(root, root);
  return decode(root, value, root, { budget: { nodes: 0, bytes: 0 }, active: /* @__PURE__ */ new Set(), references: /* @__PURE__ */ new Map() }, 0);
}

// pinned:evidence/tas/source/src/core/workflow/operationService.ts
var privateKey = /^0x[0-9a-fA-F]{64}$/;
var zeroAddress = `0x${"0".repeat(40)}`;
function fail(code) {
  const messages = {
    AUTHORIZATION_DENIED: "The configured Agent is not authorized for this Workflow operation.",
    CREDENTIAL_REQUIRED: "A valid inline EVM credential is required.",
    EXTERNAL_UNAVAILABLE: "The Workflow operation could not be completed.",
    INVALID_ARGUMENT: "The Workflow invocation arguments are invalid.",
    MANIFEST_BINDING_UNSUPPORTED: "The requested Workflow binding is unavailable.",
    OPERATION_OUTCOME_UNKNOWN: "The submitted Workflow operation outcome is unknown.",
    WALLET_MISMATCH: "The credential does not match the configured Agent wallet."
  };
  throw new TasError(code, messages[code]);
}
function ownData(value, key) {
  if (value === null || typeof value !== "object" || Array.isArray(value) || isProxy2(value)) return void 0;
  try {
    const prototype = Object.getPrototypeOf(value);
    if (prototype !== Object.prototype && prototype !== null) return void 0;
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    return descriptor !== void 0 && descriptor.enumerable && "value" in descriptor ? descriptor.value : void 0;
  } catch {
    return void 0;
  }
}
function inspectInvocation(value) {
  if (value === null || typeof value !== "object" || Array.isArray(value) || isProxy2(value)) {
    return fail("INVALID_ARGUMENT");
  }
  try {
    const prototype = Object.getPrototypeOf(value);
    const keys = Reflect.ownKeys(value);
    if (prototype !== Object.prototype && prototype !== null || keys.length !== 2 || keys.some((key) => key !== "toolName" && key !== "arguments")) return fail("INVALID_ARGUMENT");
    const toolName = Object.getOwnPropertyDescriptor(value, "toolName");
    const arguments_ = Object.getOwnPropertyDescriptor(value, "arguments");
    if (toolName === void 0 || arguments_ === void 0 || !toolName.enumerable || !arguments_.enumerable || !("value" in toolName) || !("value" in arguments_) || typeof toolName.value !== "string") return fail("INVALID_ARGUMENT");
    return { toolName: toolName.value, arguments: arguments_.value };
  } catch (error) {
    if (error instanceof TasError) throw error;
    return fail("INVALID_ARGUMENT");
  }
}
function splitArguments(value, credentialExpected) {
  if (value === null || typeof value !== "object" || Array.isArray(value) || isProxy2(value)) {
    return fail("INVALID_ARGUMENT");
  }
  let prototype;
  let descriptors;
  let keys;
  try {
    prototype = Object.getPrototypeOf(value);
    descriptors = Object.getOwnPropertyDescriptors(value);
    keys = Reflect.ownKeys(value);
  } catch {
    return fail("INVALID_ARGUMENT");
  }
  if (prototype !== Object.prototype && prototype !== null) return fail("INVALID_ARGUMENT");
  const parameters = /* @__PURE__ */ Object.create(null);
  let credential;
  let hasCredential = false;
  for (const key of keys) {
    if (typeof key !== "string") return fail("INVALID_ARGUMENT");
    const descriptor = descriptors[key];
    if (descriptor === void 0 || !descriptor.enumerable || !("value" in descriptor)) return fail("INVALID_ARGUMENT");
    if (key === "credential") {
      if (!credentialExpected) return fail("INVALID_ARGUMENT");
      credential = descriptor.value;
      hasCredential = true;
      continue;
    }
    Object.defineProperty(parameters, key, {
      configurable: true,
      enumerable: true,
      value: descriptor.value,
      writable: true
    });
  }
  return { parameters, credential, hasCredential };
}
function credentialSecret(value, present) {
  if (!present || value === null || typeof value !== "object" || Array.isArray(value) || isProxy2(value)) {
    return fail("CREDENTIAL_REQUIRED");
  }
  try {
    const prototype = Object.getPrototypeOf(value);
    const keys = Reflect.ownKeys(value);
    if (prototype !== Object.prototype && prototype !== null || keys.length !== 2 || keys.some((key) => key !== "type" && key !== "secret")) return fail("CREDENTIAL_REQUIRED");
    const type = Object.getOwnPropertyDescriptor(value, "type");
    const secret = Object.getOwnPropertyDescriptor(value, "secret");
    if (type === void 0 || secret === void 0 || !type.enumerable || !secret.enumerable || !("value" in type) || !("value" in secret) || type.value !== "inline" || typeof secret.value !== "string" || !privateKey.test(secret.value)) return fail("CREDENTIAL_REQUIRED");
    return secret.value;
  } catch (error) {
    if (error instanceof TasError) throw error;
    return fail("CREDENTIAL_REQUIRED");
  }
}
function canonicalAddress(value, failure) {
  if (typeof value !== "string") return fail(failure);
  try {
    const normalized = getAddress(value);
    if (normalized.toLowerCase() === zeroAddress) return fail(failure);
    return normalized;
  } catch (error) {
    if (error instanceof TasError) throw error;
    return fail(failure);
  }
}
function selectorMatches(selector, resolved) {
  return resolved.resolution.chain.block_hash.toLowerCase() === selector.blockHash.toLowerCase();
}
async function currentMemberWallet(options, context, signal) {
  let resolved;
  try {
    resolved = signal === void 0 ? await options.memberResolver.getAgent(options.agentId, context.blockSelector) : await options.memberResolver.getAgent(options.agentId, context.blockSelector, { signal });
  } catch (error) {
    if (signal?.aborted && error instanceof Error && error.name === "AbortError") throw error;
    return fail("EXTERNAL_UNAVAILABLE");
  }
  if (!selectorMatches(context.blockSelector, resolved)) return fail("AUTHORIZATION_DENIED");
  const projection = ownData(resolved, "data");
  if (ownData(projection, "agent_id") !== options.agentId || ownData(projection, "is_member") !== true) {
    return fail("AUTHORIZATION_DENIED");
  }
  return canonicalAddress(ownData(projection, "authentication_wallet"), "AUTHORIZATION_DENIED");
}
function decodeParameters(entry, parameters) {
  try {
    const decoded = decodeBySchema(entry.input_schema, parameters);
    if (decoded === null || typeof decoded !== "object" || Array.isArray(decoded)) return fail("INVALID_ARGUMENT");
    return decoded;
  } catch (error) {
    if (error instanceof TasError) throw error;
    return fail("INVALID_ARGUMENT");
  }
}
function inputValue(decoded, name) {
  const descriptor = Object.getOwnPropertyDescriptor(decoded, name);
  return descriptor !== void 0 && descriptor.enumerable && "value" in descriptor ? descriptor.value : void 0;
}
function sourceFailure(entry) {
  if (entry.operation.completion === "external_handle") return fail("OPERATION_OUTCOME_UNKNOWN");
  return fail("EXTERNAL_UNAVAILABLE");
}
async function resolveContractAddress(options, entry, context) {
  try {
    return canonicalAddress(await options.contractAddressResolver.resolve(entry, context), "AUTHORIZATION_DENIED");
  } catch (error) {
    if (error instanceof TasError && error.code !== "AUTHORIZATION_DENIED") throw error;
    return fail("EXTERNAL_UNAVAILABLE");
  }
}
function createWorkflowOperationService(options) {
  const dependencies = Object.freeze({
    agentId: options.agentId,
    gate: options.gate,
    registry: options.registry,
    memberResolver: options.memberResolver,
    contractAddressResolver: options.contractAddressResolver,
    client: options.client
  });
  return Object.freeze({
    async invoke(invocation, operationOptions) {
      const verified = await dependencies.gate.assertCurrent(operationOptions?.signal);
      const inspected = inspectInvocation(invocation);
      const entry = dependencies.registry.get(inspected.toolName);
      if (entry === void 0 || entry.binding.kind !== "function" && entry.binding.kind !== "class_method") {
        return fail("MANIFEST_BINDING_UNSUPPORTED");
      }
      const credentialExpected = entry.credential === "evm_private_key";
      const split = splitArguments(inspected.arguments, credentialExpected);
      const decoded = decodeParameters(entry, split.parameters);
      let secret;
      let account;
      try {
        if (credentialExpected) {
          if (entry.binding.kind !== "class_method") return fail("MANIFEST_BINDING_UNSUPPORTED");
          secret = credentialSecret(split.credential, split.hasCredential);
          try {
            account = dependencies.client.accountFromPrivateKey(secret);
          } catch {
            return fail("CREDENTIAL_REQUIRED");
          }
          canonicalAddress(account.address, "CREDENTIAL_REQUIRED");
        }
        let contractAddress;
        if (entry.runtime_dependencies.includes("contract_address")) {
          contractAddress = await resolveContractAddress(dependencies, entry, verified);
        }
        if (entry.binding.kind === "class_method") {
          const authenticationWallet = await currentMemberWallet(dependencies, verified, operationOptions?.signal);
          if (credentialExpected) {
            const signer = canonicalAddress(account?.address, "CREDENTIAL_REQUIRED");
            if (signer.toLowerCase() !== authenticationWallet.toLowerCase()) return fail("WALLET_MISMATCH");
          } else {
            try {
              account = dependencies.client.accountFromAddress(authenticationWallet);
            } catch {
              return fail("EXTERNAL_UNAVAILABLE");
            }
            let readAccount;
            try {
              readAccount = canonicalAddress(account.address, "AUTHORIZATION_DENIED");
            } catch {
              return fail("EXTERNAL_UNAVAILABLE");
            }
            if (readAccount.toLowerCase() !== authenticationWallet.toLowerCase()) return fail("EXTERNAL_UNAVAILABLE");
          }
        }
        const orderedArguments = entry.binding.arguments.map((argument) => {
          if (argument.kind === "input") return inputValue(decoded, argument.name);
          if (contractAddress === void 0) return fail("MANIFEST_BINDING_UNSUPPORTED");
          return { rpcUrl: verified.rpcUrl, address: contractAddress };
        });
        const invocationContext = {
          chainId: verified.chainId,
          rpcUrl: verified.rpcUrl,
          ...contractAddress === void 0 ? {} : { contractAddress },
          ...account === void 0 ? {} : { account }
        };
        try {
          const result = await dependencies.client.invoke(entry, orderedArguments, invocationContext);
          const encoded = encodeEvmJson(result);
          decodeBySchema(entry.output_schema, encoded);
          return encoded;
        } catch (error) {
          if (error instanceof TasError && error.code === "MANIFEST_BINDING_UNSUPPORTED") {
            return fail("MANIFEST_BINDING_UNSUPPORTED");
          }
          return sourceFailure(entry);
        }
      } finally {
        account = void 0;
        secret = void 0;
      }
    }
  });
}

// pinned:evidence/tas/source/src/core/workflow/contractAddressResolver.ts
function createWorkflowContractAddressResolver() {
  return Object.freeze({
    async resolve(entry, context) {
      if (entry.source.entrypoint === "./execution/ERC8301") return context.workflowAddress;
      throw new TasError(
        "MANIFEST_BINDING_UNSUPPORTED",
        "The requested Workflow binding has no authoritative contract address."
      );
    }
  });
}
export {
  createWorkflowContractAddressResolver,
  createWorkflowOperationService,
  createWorkflowSourceGate
};
