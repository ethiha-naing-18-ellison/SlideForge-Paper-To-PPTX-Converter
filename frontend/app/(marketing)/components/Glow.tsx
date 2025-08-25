export default function Glow() {
  return (
    <>
      {/* Top glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-gradient-to-b from-indigo-600/30 via-fuchsia-600/20 to-transparent blur-3xl pointer-events-none" />
      
      {/* Bottom glow */}
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-gradient-to-t from-cyan-500/20 via-fuchsia-600/10 to-transparent blur-3xl pointer-events-none" />
      
      {/* Side glows */}
      <div className="absolute top-1/2 left-0 w-[400px] h-[400px] bg-gradient-to-r from-indigo-600/20 to-transparent blur-3xl pointer-events-none" />
      <div className="absolute top-1/2 right-0 w-[400px] h-[400px] bg-gradient-to-l from-cyan-500/20 to-transparent blur-3xl pointer-events-none" />
    </>
  )
}



