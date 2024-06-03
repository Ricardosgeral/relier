import HeaderBox from "@/components/header-box";
import SearchInput from "@/components/search-input";
import { currentUser } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function Dams() {
  const user = await currentUser(); // uses auth from lib for rendering in server components

  if (!user) redirect("/auth/login"); //middleware should avoid this but
  return (
    <section className="no-scrollbar flex w-full flex-row max-xl:max-h-screen">
      <div className="no-scrollbar flex w-full flex-1 flex-col md:py-5 md:px-8 py-4 px-2 xl:max-h-screen">
        <header className="flex flex-col justify-between">
          <HeaderBox
            type="title"
            title="Dams in Portugal"
            subtext="Database of main dams"
          ></HeaderBox>
          <SearchInput />
        </header>
      </div>
    </section>
  );
}
