using System;
using System.Collections;
using System.IO;
using System.Threading;

namespace SmellsExample
{
    public class Account
    {
        public int Balance;                     // public field
        public static int Counter;              // mutable public static
        private ArrayList history = new ArrayList();

        public void Print() { Console.WriteLine("Account"); }

        public override bool Equals(object obj) { return base.Equals(obj); }

        public void Transaction(double value, string text)
        {
            if (value == 0.0)                   // float with ==
            {
                return;
            }

            int n = int.Parse(text);            // Parse outside try

            lock (this)                         // lock(this)
            {
                Counter = Counter + n;
            }

            try
            {
                StreamWriter sw = new StreamWriter("log.txt");
                sw.WriteLine("lock(this) { throw ex; } this is in a string and must not match");
            }
            catch (Exception ex)
            {
                throw ex;
            }
            try { int m = int.Parse(text); }    // Parse inside try: ok
            catch { }                           // empty catch
        }
    }

    public class Savings : Account
    {
        public new void Print() { Console.WriteLine("Savings"); }
    }
}
