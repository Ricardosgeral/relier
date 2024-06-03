export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <div className="relative h-screen flex items-center justify-center overflow-hidden border-t">
        <div className="absolute top-0 -z-10 h-full w-full bg-white">
          <div
            className="w-full min-h-screen flex flex-col  gap-y-10 items-center
    bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-yellow-400 to-yellow-600"
          ></div>
        </div>

        <div className="relative z-10 ">{children}</div>
      </div>
    </>
  );
}

// bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-yellow-400 to-yellow-500
