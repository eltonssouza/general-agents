import { cookies, headers } from 'next/headers';
import Link from 'next/link';
import Image from 'next/image';
import dynamic from 'next/dynamic';
import { revalidateTag } from 'next/cache';
import { ImageResponse } from 'next/server';
import { Inter } from '@next/font/google';

const Chart = dynamic(() => import('./chart'), { ssr: false });
export const runtime = 'experimental-edge';
export const metadata = { title: 'x', themeColor: '#fff', viewport: 'width=device-width' };

export default async function Page({ params, searchParams }) {
  const store = cookies();
  const h = await headers();
  const slug = params.slug;
  const q = searchParams.q;
  const res = await fetch('https://api.example.com/posts');
  revalidateTag('posts');
  // cookies() in a comment does not count
  return (
    <main>
      <Link href="/about"><a>About</a></Link>
      <Image src="/foto.png?v=2" width={10} height={10} />
      <Image src="/ok.png" alt="ok" width={10} height={10} />
    </main>
  );
}
