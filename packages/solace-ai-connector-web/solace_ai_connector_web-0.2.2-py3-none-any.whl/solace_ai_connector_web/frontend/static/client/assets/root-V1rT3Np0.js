import{r as i,j as t}from"./jsx-runtime-CNvHvvCs.js";import{C as h}from"./ConfigProvider-Du21v841.js";import{u as d,d as y,e as x,O as g}from"./index-5y0-HiVp.js";import{f as S,_ as w,M as j,L as k,S as M}from"./components-CZgPMZIv.js";/**
 * @remix-run/react v2.15.3
 *
 * Copyright (c) Remix Software Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.md file in the root directory of this source tree.
 *
 * @license MIT
 */let a="positions";function O({getKey:e,...l}){let{isSpaMode:c}=S(),r=d(),p=y();x({getKey:e,storageKey:a});let u=i.useMemo(()=>{if(!e)return null;let s=e(r,p);return s!==r.key?s:null},[]);if(c)return null;let m=((s,f)=>{if(!window.history.state||!window.history.state.key){let o=Math.random().toString(32).slice(2);window.history.replaceState({key:o},"")}try{let n=JSON.parse(sessionStorage.getItem(s)||"{}")[f||window.history.state.key];typeof n=="number"&&window.scrollTo(0,n)}catch(o){console.error(o),sessionStorage.removeItem(s)}}).toString();return i.createElement("script",w({},l,{suppressHydrationWarning:!0,dangerouslySetInnerHTML:{__html:`(${m})(${JSON.stringify(a)}, ${JSON.stringify(u)})`}}))}const _=()=>[{rel:"preconnect",href:"https://fonts.googleapis.com"},{rel:"preconnect",href:"https://fonts.gstatic.com",crossOrigin:"anonymous"},{rel:"stylesheet",href:"https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap"}];function C({children:e}){return t.jsxs("html",{lang:"en",children:[t.jsxs("head",{children:[t.jsx("meta",{charSet:"utf-8"}),t.jsx("meta",{name:"viewport",content:"width=device-width, initial-scale=1"}),t.jsx(j,{}),t.jsx(k,{})]}),t.jsxs("body",{children:[t.jsx(h,{children:e}),t.jsx(O,{}),t.jsx(M,{})]})]})}function E(){return t.jsx(g,{})}export{C as Layout,E as default,_ as links};
