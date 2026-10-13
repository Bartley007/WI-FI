// All website routes are defined here.
//
// HashRouter is used on purpose: the address looks like /#/module/fall_detection, so the built
// files in dist/ open from any static host or from the file system without server rewrite rules.
// To switch to clean URLs, replace HashRouter with BrowserRouter and add a rewrite to index.html on the host.
//
// Module pages are not listed by hand: every folder in src/modules/ gets /module/<folder name> automatically.
import { HashRouter, Routes, Route } from 'react-router-dom'
import Layout from './Layout.jsx'
import LandingPage from '../features/landing/LandingPage.jsx'
import FusionPage from '../features/fusion/FusionPage.jsx'
import { MODULES } from '../modules/registry.js'

export default function AppRouter() {
  return (
    <HashRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<LandingPage />} />                     {/* /#/                        */}
          <Route path="fusion" element={<FusionPage />} />              {/* /#/fusion                  */}
          {MODULES.map((m) => (
            <Route key={m.id} path={`module/${m.id}`} element={<m.Page />} />  // /#/module/<folder name>
          ))}
          <Route path="*" element={<LandingPage />} />
        </Route>
      </Routes>
    </HashRouter>
  )
}
