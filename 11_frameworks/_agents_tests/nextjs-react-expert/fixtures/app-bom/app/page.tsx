import { cookies } from 'next/headers';
import Image from 'next/image';
import { revalidateTag } from 'next/cache';
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const store = await cookies();
  revalidateTag('posts', 'max');
  const res = await fetch('https://api.example.com/x', { cache: 'no-store' });
  return <main><Image src="/a.png" alt="a" width={1} height={1} />{slug}{store.get('t')?.value}</main>;
}
