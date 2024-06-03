import { UserAvatar } from "./auth/user-avatar";
import SearchInput from "./search-input";

interface HeaderBoxProps {
  type?: "title" | "greeting";
  title: string;
  subtext: string;
  user?: string;
}

const HeaderBox = ({
  type = "title",
  title,
  subtext,
  user,
}: HeaderBoxProps) => {
  return (
    <div className="flex justify-between items-stretch">
      <div className="flex flex-row md:flex-col gap-y-1 gap-x-3 items-baseline justify-between">
        <h1 className="text-xl md:text-xl font-semibold text-slate-800">
          {title}
          {type === "greeting" && (
            <span className="text-20 lg:text-32 font-sans font-semibold text-yellow-500">
              &nbsp;{user}
            </span>
          )}
        </h1>
        <p className="text-sm md:text-md  text-slate-500 font-semibold">
          {subtext}
        </p>
      </div>
      <SearchInput />
      <div className="hidden md:block">
        <UserAvatar isPhotoLeft={false} />
      </div>
    </div>
  );
};

export default HeaderBox;
