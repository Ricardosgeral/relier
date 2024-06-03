import HeaderBox from "@/components/header-box";
import SearchInput from "@/components/search-input";

export default function Home() {
  return (
    <section className="no-scrollbar flex w-full flex-row max-xl:max-h-screen">
      <div className="no-scrollbar flex w-full flex-1 flex-col md:py-5 md:px-8 py-4 px-2 xl:max-h-screen">
        <header className="flex flex-col justify-between">
          <HeaderBox type="title" title="Hi" subtext="Welcome back"></HeaderBox>
        </header>
      </div>
    </section>
  );
}
